from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models

from accounts.utils import image_compress


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_banned", False)
        return self.create_user(email, username, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'webp', 'jpeg', 'gif'))]
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.__profile_picture = self.profile_picture if self.id else None

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.username

    # def save(self, *args, **kwargs):
    #     """
    #     Сохранение полей модели при их отсутствии заполнения
    #     """
    #     if self.__profile_picture != self.profile_picture and self.profile_picture:
    #         image_compress(self.profile_picture.path, width=500, height=500)


class Ban(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    reason = models.CharField(max_length=100)
    banned_at = models.DateTimeField(auto_now_add=True)


User = get_user_model()


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    profile = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="profile_comments"
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
