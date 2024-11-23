from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from nlp.models import Tag
from .forms import TagAssignmentForm

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
    tags = user_profile.soft_tags.all()  # This will give you a queryset of Tag instances
    tag_names = [tag.name for tag in tags]
    user_profile.save()
    
    # If it's a POST request, process the form
    if request.method == 'POST':
        form = TagAssignmentForm(request.POST)
        if form.is_valid():
            # Get the selected tags from the form
            selected_tags = form.cleaned_data['selected_tags']

            # Assuming each tag is a string, you can get the Tag objects from the database
            tags = Tag.objects.filter(name__in=selected_tags)

            # Save tags to the user profile (or wherever you want)
            user_profile = UserProfile.objects.get(user=request.user)
            user_profile.soft_tags.set(tags)  # Assuming `tags` is a ManyToManyField in the profile mode
            # Redirect to a success page or reload the page
            return redirect('user:profile')  # Change this to the appropriate URL

    else:
        form = TagAssignmentForm()
           
    return render(request, "profile.html", {"user_profile": user_profile, "tags": tag_names, "form": form})

