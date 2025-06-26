from django.db import models
from django.conf import settings
from django.utils.text import slugify

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/%y%m%d')
    title = models.CharField(max_length=200)
    caption = models.TextField(blank=True)
    slug = models.SlugField(max_length=200, blank=True, unique=True)
    created = models.DateField(auto_now_add=True)
    liked_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='post_liked',
        blank=True
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)  # For moderation control

    class Meta:
        ordering = ('created',)

def __str__(self):
    user_str = self.user.username if self.user else "Unknown User"
    return f"{user_str}: {self.content[:20]}"

