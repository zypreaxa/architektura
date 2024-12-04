from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from nlp.models import Tag, Recipe
from .forms import TagAssignmentForm, StrictForm

# Registration view
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Create the user and log them in
            user = form.save()
            login(request, user)

            # Create a UserProfile for the new user
            UserProfile.objects.create(user=user, preferred_cuisine="Italian", preferred_recipe_type="Vegan")

            return redirect("frontend:index")
    else:
        form = UserCreationForm()
    return render(request, "register.html", { "form": form })

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("frontend:index")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", { "form": form })

def logout_view(request):
    if request.method=="POST":
        logout(request)
        return redirect("frontend:index")
        
@login_required(login_url="/user/login/")
def profile_view(request):
    user_profile = UserProfile.objects.get(user=request.user)
    soft_tags = user_profile.soft_tags.all()  # Get the soft tags
    strict_tags = user_profile.strict_tags.all()  # Get the strict tags

    if request.method == 'POST':
        soft_form = TagAssignmentForm(request.POST, prefix="soft")
        strict_form = StrictForm(request.POST, prefix="strict")
        
        if soft_form.is_valid() and strict_form.is_valid():
            # Handle soft preferences
            selected_soft_tags = soft_form.cleaned_data['selected_tags']
            soft_tags = Tag.objects.filter(name__in=selected_soft_tags)
            user_profile.soft_tags.set(soft_tags)

            # Handle strict preferences
            selected_strict_tags = strict_form.cleaned_data['selected_tags']
            strict_tags = Tag.objects.filter(name__in=selected_strict_tags)
            user_profile.strict_tags.set(strict_tags)

            # Redirect after successful submission
            return redirect('user:profile')

    else:
        soft_form = TagAssignmentForm(prefix="soft")
        strict_form = StrictForm(prefix="strict")

    return render(request, "profile.html", {
        "user_profile": user_profile,
        "soft_tags": soft_tags,
        "strict_tags": strict_tags,
        "soft_form": soft_form,
        "strict_form": strict_form,
    })

@login_required
def manage_recipes(request):
    recipes = Recipe.objects.all()
    return render(request, "recipe_manage.html", {"recipes": recipes})
# def add_recipe
# def remove_recipe
# def edit_recipe