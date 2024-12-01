from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Q
from .spacy_processor import process_chat_message  # Import the function from spacy_processor.py
from nlp.models import Recipe
from user.models import UserProfile  # Assuming your UserProfile model is in the 'user' app

@csrf_exempt  # Only use this if CSRF tokens are causing issues; it's recommended to keep CSRF enabled
def process_chat(request):
    if request.method == "POST":
        try:
            # Parse JSON data from the request body
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON format"}, status=400)

            # Validate that "message" is present and is a non-empty string
            message = data.get("message", "")
            if not isinstance(message, str) or not message.strip():
                return JsonResponse({"error": "Message must be a non-empty string"}, status=400)

            # Process the message with spaCy to extract relevant entities
            parsed_data = process_chat_message(message)
            entities = parsed_data.get("entities", [])

            # Extract tag names from entities
            tag_names = [
                ent[0] for ent in entities if ent[1] in [
                    "COOKING_TIME", "SERVING_SIZE", "INGREDIENT", "METHOD",
                    "FLAVOR_PROFILE", "MEAL_TYPE", "DIETARY", "QUANTITY", "TEMPERATURE"
                ]
            ]

            if not tag_names:
                return JsonResponse({"recipes": []})  # No tags, no recipes

            # Build a case-insensitive query using Q objects
            query = Q()
            for tag in tag_names:
                query |= Q(tags__name__iexact=tag)

            # Query recipes based on extracted tags
            matched_recipes = Recipe.objects.filter(query).distinct()

            # Fetch user profile to apply strict and soft preference filtering
            soft_preference_tags = []
            if request.user.is_authenticated:
                try:
                    user_profile = UserProfile.objects.get(user=request.user)
                    strict_tag_names = user_profile.strict_tags.values_list("name", flat=True)

                    # Exclude recipes with strict tags
                    strict_query = Q()
                    for strict_tag in strict_tag_names:
                        strict_query |= Q(tags__name__iexact=strict_tag)
                    matched_recipes = matched_recipes.exclude(strict_query)

                    # Get soft preference tags
                    soft_preference_tags = user_profile.soft_tags.values_list("name", flat=True)
                except UserProfile.DoesNotExist:
                    pass  # Skip if no user profile

            # Prepare response data, flagging recipes that match soft preferences
            recipe_data = []
            for recipe in matched_recipes:
                recipe_tags = recipe.tags.values_list("name", flat=True)
                matches_soft_preference = any(tag in soft_preference_tags for tag in recipe_tags)
                recipe_data.append({
                    "id": recipe.id,
                    "name": recipe.name,
                    "matches_soft_preference": matches_soft_preference  # Highlight flag
                })

            # Sort recipes so that highlighted ones appear first
            sorted_recipe_data = sorted(
                recipe_data, key=lambda x: x["matches_soft_preference"], reverse=True
            )

            return JsonResponse({"recipes": sorted_recipe_data})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "POST request required"}, status=400)
