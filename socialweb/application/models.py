from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from calendar import month_name
from django.core.validators import FileExtensionValidator

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    SEX = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    DATE = [(i, i) for i in range(1, 32)]
    MONTH = [(month_name[i], month_name[i]) for i in range(1, 13)]
    YEAR = reversed([(i, i) for i in range(1950, 2006)])

    email = models.CharField(_("email address"), unique=True, max_length=100)
    phone_number = models.CharField(_('phone number'), unique=True, max_length=15)
    date_joined = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    name = models.CharField(blank=False, max_length=100)
    surname = models.CharField(blank=False, max_length=100)
    profile_picture = models.ImageField(upload_to='prof_pipcs', null=True, default="static/img/default-pic.png")
    sex = models.CharField(choices=SEX, default='F', max_length=7)
    birthday = models.IntegerField(choices=DATE, default=1)
    birthday_month = models.CharField(choices=MONTH, default=1, max_length=20)
    birthday_year = models.IntegerField(choices=YEAR, default=2005)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone number']

    def __str__(self):
        return self.email

class BlogModel(models.Model):
    post_author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post_text = models.CharField(max_length=150, blank=True)
    post_content = models.FileField(upload_to='blog_content', blank=True)
    date = models.DateTimeField(default=timezone.now())
    post_location_id = models.IntegerField()

    def __str__(self):
        return self.pk

class BlogInteractiveModel(models.Model):
    post = models.ForeignKey(BlogModel, on_delete=models.CASCADE)
    who_likes = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    content_category = models.CharField(max_length=100)

class BlogCommentsModel(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.CharField(max_length=150, blank=True)
    content = models.FileField(upload_to='comment_content', blank=True)
    date = models.DateTimeField(default=timezone.now())
    location_id = models.IntegerField()
    post = models.ForeignKey(BlogModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.post


class Videos(models.Model):
    page = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(
        upload_to='video/',
        validators=[FileExtensionValidator(allowed_extensions=['mp4'])]
    )

    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        self.title


class PhotoGallery(models.Model):
    page = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='gallery', blank=False)
    description = models.TextField(blank=True)
    date = models.DateTimeField(default=timezone.now(), null=True)

class FriendsList(models.Model):
    STATUS = [('S', 'Invite sended'), ('A', 'accepted'), ('U', 'Unaccepted'), ('N', None)]
    friends_list = models.ManyToManyField(CustomUser)
    acception = models.CharField(choices=STATUS, default='N', max_length=100)
    sender = models.IntegerField()


class ChatModel(models.Model):
    members = models.ManyToManyField(CustomUser)

class Message(models.Model):
    chat = models.ForeignKey(ChatModel, on_delete=models.CASCADE, null=True)
    message = models.CharField(max_length=100, null=True)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(default=timezone.now())


