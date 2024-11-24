from django import forms
from nlp.models import Tag

class TagAssignmentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Dynamically fetch valid tags with a tag_type
        valid_tags = Tag.objects.exclude(tag_type__isnull=True).exclude(tag_type="")
        
        # Create the choices list based on the valid tags
        choices = [(tag.name, tag.name) for tag in valid_tags]
        
        # Set the choices dynamically
        self.fields['selected_tags'].choices = choices

    # Define the field here; choices will be set dynamically in __init__
    selected_tags = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,  # Use a checkbox widget for multi-selection
        required=False  # Optional selection
    )
class StrictForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Dynamically fetch valid tags with a tag_type
        valid_tags = Tag.objects.exclude(tag_type__isnull=True).exclude(tag_type="")
        
        # Create the choices list based on the valid tags
        choices = [(tag.name, tag.name) for tag in valid_tags]
        
        # Set the choices dynamically
        self.fields['selected_tags'].choices = choices

    # Define the field here; choices will be set dynamically in __init__
    selected_tags = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,  # Use a checkbox widget for multi-selection
        required=False  # Optional selection
    )