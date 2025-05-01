from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User as DjangoUser
from .models import Post, Category, Comment, Like, Repost, Message, UserProfile
from .forms import CreatePostForm, CreateCategoryForm, CommentForm, MessageForm, UpdateUserProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.utils import timezone

# Shows the main page with all posts and reposts, including search functionality
def home(request):
    '''Define a view to show the 'home.html' template.'''
    template = 'project/home.html'
    # Get all posts and reposts
    posts = Post.objects.all()
    reposts = Repost.objects.all()
    
    # Handle search query
    search_query = request.GET.get('search', '')
    if search_query:
        # Search in post content and title
        posts = posts.filter(
            models.Q(content__icontains=search_query) |
            models.Q(title__icontains=search_query)
        ).distinct()
        # Search in repost commentary
        reposts = reposts.filter(commentary__icontains=search_query)
    
    # Handle category filter
    category_id = request.GET.get('category')
    if category_id:
        posts = posts.filter(category_id=category_id)
        # For reposts, filter by the original post's category
        reposts = reposts.filter(original_post__category_id=category_id)
    
    # Create a list of tuples (object, created_at, is_repost)
    post_list = [(post, post.created_at, False) for post in posts]
    repost_list = [(repost, repost.created_at, True) for repost in reposts]
    
    # Combine posts and reposts
    combined_list = post_list + repost_list
    
    # Sort based on the sort parameter
    sort_type = request.GET.get('sort', 'latest')
    if sort_type == 'oldest':
        combined_list = sorted(combined_list, key=lambda x: x[1])
    elif sort_type == 'popular':
        combined_list = sorted(combined_list, key=lambda x: x[0].like_count if not x[2] else x[0].original_post.like_count, reverse=True)
    elif sort_type == 'dialogue':
        combined_list = sorted(combined_list, key=lambda x: x[0].comment_count() if not x[2] else x[0].original_post.comment_count(), reverse=True)
    else:  # latest
        combined_list = sorted(combined_list, key=lambda x: x[1], reverse=True)
    
    context = {
        'posts': combined_list,
        'search_query': search_query,
        'categories': Category.objects.all().order_by('name')  
    }
    return render(request, template, context)

# Shows a user's profile page with their information
class ShowUserPageView(DetailView):
    """
    View to display the details of a single user profile.
    Uses a DetailView to retrieve and display a specific User object.
    """
    model = DjangoUser
    template_name = 'project/show_user.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the Django user for comparison
        context['django_user'] = self.request.user
        # Add the profile image update form
        context['form'] = UpdateUserProfileForm()
        return context

# Shows all posts in the system, with options to filter by user, comments, or likes
class ShowAllPostsView(ListView):

    model = Post
    template_name = 'project/show_all_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        # Get all posts and reposts
        posts = Post.objects.all()
        reposts = Repost.objects.all()
        
        # Filter by user
        user_id = self.request.GET.get('user')
        if user_id:
            posts = posts.filter(user_id=user_id)
            reposts = reposts.filter(user_id=user_id)
        
        # Filter by user's comments
        user_comments_id = self.request.GET.get('user_comments')
        if user_comments_id:
            commented_posts = Post.objects.filter(comments__user_id=user_comments_id).distinct()
            posts = commented_posts
            reposts = Repost.objects.none()
            
        # Filter by user's likes
        user_likes_id = self.request.GET.get('user_likes')
        if user_likes_id:
            liked_posts = Post.objects.filter(likes__user_id=user_likes_id).distinct()
            posts = liked_posts
            reposts = Repost.objects.none()
        
        # Filter by category
        category_id = self.request.GET.get('category')
        if category_id:
            posts = posts.filter(category_id=category_id)
            reposts = reposts.filter(original_post__category_id=category_id)
        
        # Create tuples of (object, created_at, is_repost)
        post_list = [(post, post.created_at, False) for post in posts]
        repost_list = [(repost, repost.created_at, True) for repost in reposts]
        
        # Combine and sort posts/reposts
        combined_list = post_list + repost_list
        
        # Sort by selected criteria
        sort_type = self.request.GET.get('sort', 'latest')
        if sort_type == 'oldest':
            combined_list = sorted(combined_list, key=lambda x: x[1])
        elif sort_type == 'popular':
            combined_list = sorted(combined_list, key=lambda x: x[0].like_count if not x[2] else x[0].original_post.like_count, reverse=True)
        elif sort_type == 'dialogue':
            combined_list = sorted(combined_list, key=lambda x: x[0].comment_count() if not x[2] else x[0].original_post.comment_count(), reverse=True)
        else:  # latest
            combined_list = sorted(combined_list, key=lambda x: x[1], reverse=True)
        
        return combined_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all().order_by('name')  
        # Add user info to context if filtering by user, user's comments, or user's likes
        user_id = self.request.GET.get('user')
        user_comments_id = self.request.GET.get('user_comments')
        user_likes_id = self.request.GET.get('user_likes')
        if user_id:
            context['filtered_user'] = DjangoUser.objects.get(id=user_id)
            context['filter_type'] = 'posts'
        elif user_comments_id:
            context['filtered_user'] = DjangoUser.objects.get(id=user_comments_id)
            context['filter_type'] = 'comments'
        elif user_likes_id:
            context['filtered_user'] = DjangoUser.objects.get(id=user_likes_id)
            context['filter_type'] = 'likes'
        return context

# Lets users create new categories for posts
class CreateCategoryView(CreateView):
    model = Category
    template_name = 'project/create_category.html'
    form_class = CreateCategoryForm
    context_object_name = 'category'
    success_url = reverse_lazy('create_post')

# Lets logged-in users create new posts
class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'project/create_post.html'
    form_class = CreatePostForm
    context_object_name = 'post'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# Shows a single post with all its details, comments, and interaction options
class PostDetailView(DetailView):

    model = Post
    template_name = 'project/post_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        # Increment view count when post is viewed
        post.increment_view_count()
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        if self.request.user.is_authenticated:
            context['is_liked'] = Like.objects.filter(post=post, user=self.request.user).exists()
            context['is_reposted'] = Repost.objects.filter(original_post=post, user=self.request.user).exists()
        else:
            context['is_liked'] = False
            context['is_reposted'] = False
        return context

# Logs out the current user and returns to home page
def logout_view(request):
    logout(request)
    return redirect('home')

# Lets logged-in users add comments to posts
class CreateCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'project/post_detail.html'

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.user = self.request.user
        form.instance.post = post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.kwargs['pk']})

# Lets users delete their own comments
class DeleteCommentView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'project/delete_comment.html'
    
    def get_success_url(self):
        # Get the post ID from the comment
        post_id = self.object.post.id
        return reverse_lazy('post_detail', kwargs={'pk': post_id})

# Lets users like or unlike posts
@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    
    if not created:
        # If the like already existed, remove it
        like.delete()
        post.like_count = max(0, post.like_count - 1)
    else:
        # If the like was just created, increment the count
        post.like_count += 1
    
    post.save()
    
    return redirect('post_detail', pk=post_id)

# Lets users repost or un-repost posts
@login_required
def toggle_repost(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    # Only look for non-quote reposts
    repost = Repost.objects.filter(original_post=post, user=request.user, is_quote=False).first()
    
    if repost:
        # If the repost exists, remove it
        repost.delete()
    else:
        # Create a new regular repost
        Repost.objects.create(
            original_post=post,
            user=request.user,
            is_quote=False
        )
    
    return redirect('post_detail', pk=post_id)

# Lets users create quote reposts with their own commentary
@login_required
def create_quote_repost(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        commentary = request.POST.get('commentary', '')
        # create a new quote repost
        Repost.objects.create(
            original_post=post,
            user=request.user,
            commentary=commentary,
            is_quote=True
        )
    return redirect('post_detail', pk=post_id)

# Handles new user registration
class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'project/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Log the user in after successful registration
        login(self.request, self.object)
        return response

# Lets users delete their own posts
class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'project/delete_post.html'
    success_url = reverse_lazy('home')

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)

# Lets users delete their own reposts
class DeleteRepostView(LoginRequiredMixin, DeleteView):
    model = Repost
    template_name = 'project/delete_repost.html'
    success_url = reverse_lazy('home')

    def get_queryset(self):
        return Repost.objects.filter(user=self.request.user)

# Lets users edit their own posts
class EditPostView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'project/edit_post.html'
    form_class = CreatePostForm
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.edited = True
        form.instance.edited_at = timezone.now()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})

# Shows the user's inbox with all their conversations
@login_required
def inbox(request):
    # Get all messages where user is either sender or receiver
    messages = Message.objects.filter(
        models.Q(sender=request.user) | models.Q(receiver=request.user)
    ).order_by('-created_at')

    # Group messages by conversation partner
    conversations = {}
    for message in messages:
        # Get the other user in the conversation
        other_user = message.sender if message.receiver == request.user else message.receiver
        if other_user not in conversations:
            conversations[other_user] = message

    context = {
        'conversations': conversations
    }
    return render(request, 'project/inbox.html', context)

# Shows a conversation between two users
@login_required
def conversation(request, user_id):
    other_user = get_object_or_404(DjangoUser, id=user_id)
    
    # Get all messages between the two users
    messages = Message.objects.filter(
        (models.Q(sender=request.user) & models.Q(receiver=other_user)) |
        (models.Q(sender=other_user) & models.Q(receiver=request.user))
    ).order_by('created_at')

    # Mark unread messages as read
    unread_messages = messages.filter(receiver=request.user, is_read=False)
    unread_messages.update(is_read=True)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = other_user
            message.save()
            return redirect('conversation', user_id=user_id)
    else:
        form = MessageForm()

    context = {
        'messages': messages,
        'other_user': other_user,
        'form': form
    }
    return render(request, 'project/conversation.html', context)

# Shows a page to start a new message with another user
@login_required
def new_message(request):
    users = DjangoUser.objects.exclude(id=request.user.id).order_by('username')
    return render(request, 'project/new_message.html', {'users': users})

# Lets users search for other users
@login_required
def search_users(request):
    query = request.GET.get('search', '')
    if query:
        users = DjangoUser.objects.filter(username__icontains=query).exclude(id=request.user.id)
    else:
        users = DjangoUser.objects.none()
    return render(request, 'project/search_results.html', {'users': users})

# Lets users update their profile information
class UpdateUserProfileView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UpdateUserProfileForm
    template_name = 'project/update_profile.html'

    def get_object(self, queryset=None):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile

    def get_success_url(self):
        return reverse('show_user', kwargs={'pk': self.request.user.id})

# Lets users edit their bio
@login_required
def edit_bio(request):
    if request.method == 'POST':
        bio = request.POST.get('bio', '')
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        profile.bio = bio
        profile.save()
        return redirect('show_user', pk=request.user.id)
    return render(request, 'project/edit_bio.html')