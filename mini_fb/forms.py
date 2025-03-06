from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
# Form for creating a new user profile.

    class Meta:
        model = Profile
        fields = ['first_name','last_name','city','email', 'profile_image_url']

class CreateStatusMessageForm(forms.ModelForm):
# Form for creating a new status message.

    class Meta:
        
        model = StatusMessage
        fields = ['message']

class UpdateProfileForm(forms.ModelForm):
# Form for updating profile attributes

    class Meta:
        model = Profile
        fields = ['city', 'email', 'profile_image_url']
