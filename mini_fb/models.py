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
    
    def get_friends(self):
        """Return a list of Profile instances representing this user's friends."""
        friends = Friend.objects.filter(models.Q(profile1=self) | models.Q(profile2=self))
        return [friend.profile2 if friend.profile1 == self else friend.profile1 for friend in friends]
    
    def add_friend(self, other):
        """Add a friend relationship between self and another Profile.
        """
        if self == other:
            return  # Prevents selffriending

        # Check if a friendship already exists
        existing_friendship = Friend.objects.filter(
            models.Q(profile1=self, profile2=other) | models.Q(profile1=other, profile2=self)
        ).exists()

        if not existing_friendship:
            Friend.objects.create(profile1=self, profile2=other)
    
    def get_friend_suggestions(self):
        """
        Returns a list of suggested friends (Profiles) for this Profile.
        Suggestions are based on "friends of friends" who are not already friends with self.
        """
        current_friends = self.get_friends()

        # Get friends of friends
        friends_of_friends = Profile.objects.filter(
            models.Q(profile1__profile2__in=current_friends) | models.Q(profile2__profile1__in=current_friends)
        ).exclude(pk=self.pk).exclude(pk__in=[friend.pk for friend in current_friends]).distinct()

        return friends_of_friends
    
    def get_news_feed(self):

        friends = self.get_friends()

        news_feed = StatusMessage.objects.filter(
            models.Q(profile=self) | models.Q(profile__in=friends)
        ).order_by('-timestamp')  

        return news_feed




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
    
    def get_images(self):
        """Return all images associated with this StatusMessage."""
        return Image.objects.filter(statusimage__status_message=self)

    
class Image(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image_file = models.ImageField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    caption = models.TextField(blank=True, null=True)  # Optional description

    def __str__(self):
        return f'Image uploaded by {self.profile.first_name}'

class StatusImage(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE)

    def __str__(self):
        return f'Image associated with status: {self.status_message}'
    
class Friend(models.Model):
    profile1 = models.ForeignKey(Profile, related_name="profile1", on_delete=models.CASCADE)
    profile2 = models.ForeignKey(Profile, related_name="profile2", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Friends {self.profile1.first_name} & {self.profile2.first_name}'