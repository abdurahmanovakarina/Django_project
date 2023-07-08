from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class CustomUserModelBackend(ModelBackend):
    def get_user_model(self):
        return get_user_model()
