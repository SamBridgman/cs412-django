
from django import forms
from .models import Post, Category, Comment, Message, UserProfile

# Form for creating new categories with name and description fields
class CreateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

# Form for creating new posts with support for custom categories and image URLs
class CreatePostForm(forms.ModelForm):
    new_category = forms.CharField(max_length=100, required=False, 
        help_text="Or create a new category")
    image_url = forms.URLField(max_length=500, required=False,
        help_text="URL of the web-hosted image (optional)",
        widget=forms.URLInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500',
            'placeholder': 'https://example.com/image.jpg'
        }))

    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'new_category', 'image_url']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500',
                'placeholder': 'Enter post title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500',
                'rows': 4,
                'placeholder': 'Write your post content here...'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500'
            })
        }

# Form for adding comments to posts with styled textarea
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500',
                'rows': 4,
                'placeholder': 'Write your comment here...'
            })
        }

# Form for sending messages between users with custom styling
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border-4 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] focus:outline-none focus:shadow-none focus:translate-x-1 focus:translate-y-1 transition-all duration-200',
                'rows': 3,
                'placeholder': 'Type your message...'
            })
        }

# Form for updating user profile information, specifically profile images
class UpdateUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_image_url']
        widgets = {
            'profile_image_url': forms.URLInput(attrs={
                'class': 'w-full px-3 py-2 border-4 border-black rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500',
                'placeholder': 'https://example.com/image.jpg'
            })
        }