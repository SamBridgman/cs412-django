"""
File: views.py
Author: Sam Bridgman
Email: bridgman@bu.edu
Description: Defines views for displaying user profiles in the Mini FB application.
Includes a ListView to display all profiles and a DetailView to show individual 
profile details.
"""

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Profile

# Create your views here.

class ShowAllProfilesView(ListView):
    """
    Displays a list of all profiles

    Attributes:
    - model: Specifies the Profile model.
    - template_name: Path to the template used for rendering.
    - context_object_name: Name of the context variable passed to the template.
    """
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles' 

class ShowProfilePageView(DetailView):
    """
    Displays the details of a single profile.

    Attributes:
    - model: Specifies the Profile model.
    - template_name: Path to the template used for rendering.
    - context_object_name: Name of the context variable passed to the template.
    """
    model = Profile
    template_name = 'mini_fb/show_profile.html'  # Reusing the same template
    context_object_name = 'profile'
