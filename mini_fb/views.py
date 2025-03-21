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
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import *
from .forms import *


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

class UpdateProfileView(UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'


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
        Saves uploaded images and links them to the status message.
        """

        print(f"CreateStatusMessageView.form_valid: form.cleaned_data={form.cleaned_data}")

        status_message = form.save(commit=False)
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        status_message.profile = profile
        status_message.save()  

        files = self.request.FILES.getlist('files')

        for file in files:
            image = Image(profile=profile, image_file=file)
            image.save()

            status_image = StatusImage(image=image, status_message=status_message)
            status_image.save()

        return super().form_valid(form)

    def get_success_url(self):
        """
        Redirects the user to the profile page after successfully creating a status message.
        """
        pk = self.kwargs['pk']
        return reverse('show_profile', kwargs={'pk':pk})

class DeleteStatusMessageView(DeleteView):
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = "StatusMessage"

    def get_success_url(self):
        """
        Redirects the user to the correct profile page after successfully deleting a status message.
        """
        pk = self.object.profile.pk 
        return reverse('show_profile', kwargs={'pk':pk})

class UpdateStatusMessageView(UpdateView):
    model = StatusMessage
    template_name = 'mini_fb/update_status_form.html'
    context_object_name = "StatusMessage"
    fields = ['message']

    def get_success_url(self):
        """
        Redirects the user to the correct profile page after successfully updating a status message.
        """
        pk = self.object.profile.pk 
        return reverse('show_profile', kwargs={'pk':pk})
    
class AddFriendView(View):
    """Handles adding a friend by updating the Friend model """

    def dispatch(self, request, *args, **kwargs):
        profile = Profile.objects.get(pk=pk)
        other_profile = profile = Profile.objects.get(pk='other_pk')

        profile.add_friend(other_profile)

        return reverse('show_profile', pk=profile.pk)
    
class ShowFriendSuggestionsView(DetailView):
    """
    View to display friend suggestions for a specific Profile.
    """
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['friend_suggestions'] = self.object.get_friend_suggestions()
        return context


class ShowNewsFeedView(DetailView):
    """
    View to display the news feed for a Profile, showing recent status messages.
    """
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        """
        Adds the news feed to the context
        """
        context = super().get_context_data(**kwargs)
        context['news_feed'] = self.object.get_news_feed()
        return context
