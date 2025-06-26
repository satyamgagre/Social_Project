from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .forms import PostCreateForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            messages.success(request, '✅ Your post has been created successfully!')
            return redirect('create')  
    else:
        form = PostCreateForm()
    return render(request, 'posts/create.html', {'form': form})

def feed(request):
    posts = Post.objects.all()
    return render(request, 'posts/feed.html',{'posts':posts})

def like_post(request):
    post_id = request.POST.get('post_id')
    post = get_object_or_404(post, id=post_id)
    if post.liked_by.filter(id=request.user.id).exists():
        post.liked_by.remove(request.user)
    else:
        post.liked_by.add(request.user)


