from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .forms import PostCreateForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import Post, Comment

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

@login_required
def like_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, id=post_id)

        liked = False
        if post.liked_by.filter(id=request.user.id).exists():
            post.liked_by.remove(request.user)
        else:
            post.liked_by.add(request.user)
            liked = True

        return JsonResponse({
            'liked': liked,
            'likes_count': post.liked_by.count()
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.post = post
        comment.save()
        return JsonResponse({
            'success': True,
            'comment': comment.body,
            'user': comment.user.username,
        })
    return JsonResponse({'success': False, 'errors': form.errors})

