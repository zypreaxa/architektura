from django import forms
from nlp.models import Tag

class TagAssignmentForm(forms.Form):
    # Retrieve all existing tags from the database
    tags = Tag.objects.all()
    
    # Dynamically create the choices list based on the tags in the database
    CHOICES = [(tag.name, tag.name) for tag in tags]

    # Use a MultipleChoiceField to allow users to select multiple tags
    selected_tags = forms.MultipleChoiceField(
        choices=CHOICES, 
        widget=forms.CheckboxSelectMultiple,  # You can also use a select widget with multiple option
        required=False  # Make it optional, or you can make it required if needed
    )
    
class StrictForm(forms.Form):
    # Retrieve all existing tags from the database
    tags = Tag.objects.all()
    
    # Dynamically create the choices list based on the tags in the database
    CHOICES = [(tag.name, tag.name) for tag in tags]

    # Use a MultipleChoiceField to allow users to select multiple tags
    selected_tags = forms.MultipleChoiceField(
        choices=CHOICES, 
        widget=forms.CheckboxSelectMultiple,  # You can also use a select widget with multiple option
        required=False  # Make it optional, or you can make it required if needed
    )