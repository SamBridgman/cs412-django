"""
File: models.py
Author: Sam Bridgman
Email: bridgman@bu.edu
Description: Defines the Profile model, which stores user profile details, including 
name, city, email, and profile image URL. This model is used to represent users 
in the Mini FB application.
"""

from django.db import models

# Create your models here.
class Profile(models.Model):
    """Encapsulate the idea of a Profile, representing a user's basic information."""

    # data attributes of a Article:
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.DateTimeField(auto_now=True)
    profile_image_url = models.URLField(blank=True) ## new
    
    def __str__(self):
        '''Return a string representation of this Profile object.'''
        return f'{self.first_name}, {self.last_name}'