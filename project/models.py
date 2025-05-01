"""
Database models for the project application.
This module defines the core data structures and relationships for the forum system,
including user profiles, posts, comments, likes, reposts, and messaging functionality.
"""

from django.db import models
from django.contrib.auth.models import User as DjangoUser
from django.core.validators import URLValidator

# Extends the default Django User model with additional profile information
# including profile image and bio
class UserProfile(models.Model):
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE, related_name='project_profile')
    profile_image_url = models.URLField(max_length=500, blank=True, null=True, validators=[URLValidator()])
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

# Organizes posts into categories for better content organization
# Each category has a unique name and optional description
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name

# Core content model representing forum posts
# Includes engagement metrics (likes, views), content, and metadata
class Post(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    edited = models.BooleanField(default=False)  
    edited_at = models.DateTimeField(null=True, blank=True)  
    like_count = models.PositiveIntegerField(default=0)
    view_count = models.PositiveIntegerField(default=0)  
    user = models.ForeignKey(DjangoUser, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts')
    title = models.CharField(max_length=200, default="Untitled Post")
    image_url = models.URLField(max_length=500, blank=True, null=True, validators=[URLValidator()], 
                               help_text="URL of the web-hosted image")

    def __str__(self):
        return f"Post {self.id} by {self.user}"

    def comment_count(self):
        return self.comments.count()

    def increment_view_count(self):
        self.view_count += 1
        self.save(update_fields=['view_count'])

# Represents user comments on posts
# Tracks creation and update timestamps for each comment
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(DjangoUser, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment {self.id} on Post {self.post.id}"

# Tracks user likes on posts
# Ensures a user can only like a post once through unique constraint
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(DjangoUser, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f"Like by {self.user} on Post {self.post.id}"

# Enables users to share existing posts
# Supports both simple reposts and quote reposts with commentary
class Repost(models.Model):
    original_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reposts')
    user = models.ForeignKey(DjangoUser, on_delete=models.CASCADE, related_name='reposts')
    commentary = models.TextField(blank=True)  # Optional commentary on the repost
    created_at = models.DateTimeField(auto_now_add=True)
    is_quote = models.BooleanField(default=False)  # True if user added commentary

    def __str__(self):
        if self.is_quote:
            return f"Quote repost by {self.user} of Post {self.original_post.id}"
        return f"Repost by {self.user} of Post {self.original_post.id}"

# Handles private messaging between users
class Message(models.Model):
    sender = models.ForeignKey(DjangoUser, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(DjangoUser, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}"
