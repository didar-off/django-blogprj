from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.utils.text import slugify
from shortuuid.django_fields import ShortUUIDField
import shortuuid


class User(AbstractUser):
    username = models.CharField(unique=True, max_length=100)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        email_username, mobile = self.email.split('@')
        if not self.full_name:
            self.full_name = email_username
        if not self.username:
            self.username = email_username

        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='image/profiles', default='default/user.jpg')
    full_name = models.CharField(max_length=100)
    bio = models.CharField(max_length=100, null=True, blank=True)
    about = models.CharField(max_length=100, null=True, blank=True)
    author = models.BooleanField(default=False)
    country = models.CharField(max_length=100, null=True, blank=True)
    facebook = models.CharField(max_length=100, null=True, blank=True)
    instagram = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    update = models.DateField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.full_name:
            self.full_name = self.user.full_name
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username
    

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)


class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.FileField(upload_to='image/categories', default='default/category.jpg')
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    def post_count(self):
        return Post.objects.filter(category=self, status='Published').count()

    def __str__(self):
        return self.title


class Post(models.Model):

    STATUS = (
        ('Published', 'Published'),
        ('Draft', 'Draft'),
        ('Disabled', 'Disabled')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile_posts')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='image/posts', default='default/post.jpg')
    status = models.CharField(choices=STATUS, max_length=100, default='Draft')
    views = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, blank=True, related_name='liked_posts')
    slug = models.SlugField(unique=True)
    date = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title) + '-' + shortuuid.uuid()[:2]
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    comment = models.TextField(null=True, blank=True)
    reply = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    update = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.post.title
    

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post.title
    

class Notification(models.Model):

    TYPE = (
        ('Like', 'Like'),
        ('Comment', 'Comment'),
        ('Bookmark', 'Bookmark')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    type = models.CharField(choices=TYPE, max_length=50)
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.post:
            return f'{self.post.title} - {self.type}'
        else:
            return 'Notification'
        
