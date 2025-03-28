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
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View, TemplateView
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin ## NEW
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


from .forms import *
from django.shortcuts import redirect


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
    model = Profile
    template_name = "mini_fb/create_profile_form.html"
    form_class = CreateProfileForm
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'user_form' not in context:
            context['user_form'] = UserCreationForm()
        return context

    def post(self, request, *args, **kwargs):
        # Create both forms with POST data
        self.object = None
        profile_form = self.get_form()
        user_form = UserCreationForm(request.POST)

        if profile_form.is_valid() and user_form.is_valid():
            # Save user and log them in
            user = user_form.save()
            login(request, user)

            # Save profile, attach user to it
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            return self.form_valid(profile_form)
        else:
            return self.form_invalid(profile_form)

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.pk})


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 
    
    def get_object(self):
        return Profile.objects.get(user=self.request.user)


class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    template_name = 'mini_fb/create_status_form.html'
    form_class = CreateStatusMessageForm

    def get_login_url(self):
        return reverse('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)
        context['profile'] = profile
        return context

    def form_valid(self, form):
        status_message = form.save(commit=False)
        profile = Profile.objects.get(user=self.request.user)
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
        profile = Profile.objects.get(user=self.request.user)
        return reverse('show_profile', kwargs={'pk': profile.pk})


class DeleteStatusMessageView(LoginRequiredMixin,DeleteView):
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = "StatusMessage"

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 

    def get_success_url(self):
        """
        Redirects the user to the correct profile page after successfully deleting a status message.
        """
        pk = self.object.profile.pk 
        return reverse('show_profile', kwargs={'pk':pk})

class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    model = StatusMessage
    template_name = 'mini_fb/update_status_form.html'
    context_object_name = "StatusMessage"
    fields = ['message']

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 

    def get_success_url(self):
        """
        Redirects the user to the correct profile page after successfully updating a status message.
        """
        pk = self.object.profile.pk 
        return reverse('show_profile', kwargs={'pk':pk})
    
class AddFriendView(LoginRequiredMixin, View):
    def get_login_url(self):
        return reverse('login')

    def dispatch(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        other_profile_pk = self.kwargs.get('other_pk')
        other_profile = Profile.objects.get(pk=other_profile_pk)

        profile.add_friend(other_profile)
        return redirect('show_profile', pk=profile.pk)

    
class ShowFriendSuggestionsView(LoginRequiredMixin, TemplateView):
    template_name = 'mini_fb/friend_suggestions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)
        context['profile'] = profile
        context['friend_suggestions'] = profile.get_friend_suggestions()
        return context



class ShowNewsFeedView(LoginRequiredMixin, TemplateView):
    template_name = 'mini_fb/news_feed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)
        context['profile'] = profile
        context['news_feed'] = profile.get_news_feed()
        return context


class LogoutConfirmationView(TemplateView):
    template_name = 'mini_fb/logged_out.html'
