from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .spacy_processor import process_chat_message  # Import the function from spacy_processor.py
from nlp.models import Recipe, Tag
from user.models import UserProfile  # Assuming your UserProfile model is in the 'user' app

@csrf_exempt  # Only use this if CSRF tokens are causing issues; it's recommended to keep CSRF enabled
def process_chat(request):
    if request.method == "POST":
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)
            message = data.get("message", "")
            
            # Process the message with spaCy to extract relevant entities
            parsed_data = process_chat_message(message)
            entities = parsed_data.get("entities", [])
            
            # Extract tag names from entities
            tag_names = [ent[0] for ent in entities if ent[1] in [
                "COOKING_TIME", "SERVING_SIZE", "INGREDIENT", "METHOD",
                "FLAVOR_PROFILE", "MEAL_TYPE", "DIETARY", "QUANTITY", "TEMPERATURE"
            ]]
          
            # Query recipes based on extracted tags
            matched_recipes = Recipe.objects.filter(tags__name__in=tag_names).distinct()

            # Apply strict tag filtering if the user is authenticated
            if request.user.is_authenticated:
                try:
                    # Fetch the user's strict tags
                    user_profile = UserProfile.objects.get(user=request.user)
                    strict_tag_names = user_profile.strict_tags.values_list("name", flat=True)
                    
                    # Exclude recipes with any of the strict tags
                    matched_recipes = matched_recipes.exclude(tags__name__in=strict_tag_names)
                except UserProfile.DoesNotExist:
                    pass  # Skip exclusion if user profile doesn't exist
            
            # Remove duplicates and prepare the response
            unique_recipes = {recipe.name: recipe for recipe in matched_recipes}.values()

            if unique_recipes:
                recipe_data = [{"name": recipe.name} for recipe in unique_recipes]
                return JsonResponse({"recipes": recipe_data})
            else:
                return JsonResponse({"recipes": []})  # Empty list if no recipes are found

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "POST request required"}, status=400)
