# forms.py
from django import forms
from .models import UserInfo, Game  # Make sure to import the Game model if needed

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['user_description', 'favorite_list', 'to_play', 'already_played']
        widgets = {
            'user_description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),  # Customize textarea appearance
            'favorite_list': forms.CheckboxSelectMultiple(),  # Use checkboxes for many-to-many fields
            'to_play': forms.CheckboxSelectMultiple(),
            'already_played': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'
        self.fields['user_description'].label = 'Description'