from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from accounts.models import CustomUser, Comment


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ["username", "email", "password1", "password2", "profile_picture"]

    username = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={"class": "form-control cp-input", "placeholder": "Enter username"}
        ),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control cp-input", "placeholder": "Enter email"}
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control cp-input", "placeholder": "Enter password"}
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control cp-input", "placeholder": "Confirm password"}
        )
    )
    profile_picture = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={"class": "form-control-file", "id": "id_profile_picture"}
        ),
    )


class CustomUserUpdateForm(forms.ModelForm):
    username = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    email = forms.EmailField(
        required=True, widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = get_user_model()
        fields = ["username", "email"]


class UpdateProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(
        required=False, widget=forms.FileInput(attrs={"class": "form-control-file"})
    )

    class Meta:
        model = CustomUser
        fields = ["profile_picture"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {"text": forms.Textarea(attrs={"class": "form-control", "rows": 3})}

    def clean_text(self):
        text = self.cleaned_data["text"]
        if len(text) < 5:
            raise forms.ValidationError("Comment is too short.")
        return text
