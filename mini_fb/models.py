"""
File: models.py
Author: Sam Bridgman
Email: bridgman@bu.edu
Description: Defines the Profile model, which stores user profile details, including 
name, city, email, and profile image URL. This model is used to represent users 
in the Mini FB application. Also displays the Status Message Model for creating messages
"""

from django.db import models
from django.urls import reverse

# Create your models here.
class Profile(models.Model):
    """Encapsulate the idea of a Profile, representing a user's basic information."""

    # data attributes of a Profile:
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.TextField(blank=False)
    profile_image_url = models.URLField(blank=True) ## new

    def get_status_messages(self):
        messages = StatusMessage.objects.filter(profile=self)
        return messages
    
    def get_absolute_url(self):
        return reverse('show_profile',kwargs={'pk':self.pk})

    def __str__(self):
        '''Return a string representation of this Profile object.'''
        return f'{self.first_name}, {self.last_name}'
    
class StatusMessage(models.Model):
    # Model to store status messages associated with user profiles.
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    message = models.TextField(blank=False)

    def __str__(self):
        return f'{self.message}'
    