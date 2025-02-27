"""
File: views.py
Author: Sam Bridgman
Email: bridgman@bu.edu
Description: Defines views for displaying user profiles in the Mini FB application.
Includes a ListView to display all profiles and a DetailView to show individual 
profile details.
"""
from django.urls import reverse
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Profile
from .forms import CreateProfileForm, CreateStatusMessageForm


class ShowAllProfilesView(ListView):
    """
    View to display all profiles in the system.
    Uses a ListView to retrieve and display all Profile objects.
    """
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles' 

class ShowProfilePageView(DetailView):
    """
    View to display the details of a single profile.
    Uses a DetailView to retrieve and display a specific Profile object.
    """
    model = Profile
    template_name = 'mini_fb/show_profile.html'  # Reusing the same template
    context_object_name = 'profile'

class CreateProfileView(CreateView):
    """
    View to handle the creation of a new profile.
    Uses a CreateView with a form to input new Profile details.
    """
    model = Profile
    template_name = "mini_fb/create_profile_form.html"
    context_object_name = 'profile'
    form_class = CreateProfileForm

class CreateStatusMessageView(CreateView):
    """
    View to handle the creation of a new status message.
    Uses a CreateView with a form to input a new StatusMessage.
    """
    template_name = 'mini_fb/create_status_form.html'
    form_class = CreateStatusMessageForm

    def get_context_data(self):
        """
        Adds the related profile to the context for use in the template.
        Retrieves the profile using the primary key (pk) from URL parameters.
        """
        context = super().get_context_data()

        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        context['profile'] = profile
        return context
    def form_valid(self, form):
        """
        Assigns the status message to the corresponding profile before saving.
        Logs the form data for debugging purposes.
        """

        print(f"CreateStatusMessageView.form_valid: form.cleaned_data={form.cleaned_data}")
        
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        form.instance.profile = profile 

        return super().form_valid(form)
    def get_success_url(self):
        """
        Redirects the user to the profile page after successfully creating a status message.
        """
        pk = self.kwargs['pk']
        return reverse('show_profile', kwargs={'pk':pk})