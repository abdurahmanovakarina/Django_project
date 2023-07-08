from django import forms
from multiupload.fields import MultiImageField
from django_ckeditor_5.widgets import CKEditor5Widget

from .models import (
    Section,
    Article,
    ArticleComment,
    Moderation,
    History,
    Role,
    UserProfile, Photo,
)


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ["title", "description", "parent"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})

        self.fields["description"].widget.attrs.update({'class': 'form-control django_ckeditor_5'})
        self.fields["description"].required = False


class ArticleCreateForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ["title", "content", "sidebar_content", "section", "main_photo", "status"]
        widgets = {
            "content": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name='extends'
            ),
            "sidebar_content": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name='extends'
            ),
            "main_photo": forms.ClearableFileInput(
                attrs={"required": False}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})

        self.fields["content"].widget.attrs.update({'class': 'form-control django_ckeditor_5'})
        self.fields["content"].required = False
        self.fields["sidebar_content"].widget.attrs.update({'class': 'form-control django_ckeditor_5'})
        self.fields["sidebar_content"].required = False


class ArticleUpdateForm(ArticleCreateForm):

    class Meta:
        model = Article
        fields = ArticleCreateForm.Meta.fields
        widgets = {
            "content": CKEditor5Widget(attrs={"class": "django_ckeditor_5"}, config_name='extends')
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['content'].widget.attrs.update({'class': 'form-control django_ckeditor_5'})
        self.fields['content'].required = False
        self.fields["sidebar_content"].widget.attrs.update({'class': 'form-control django_ckeditor_5'})
        self.fields["sidebar_content"].required = False


class ArticleCommentForm(forms.ModelForm):
    class Meta:
        model = ArticleComment
        fields = ["content"]


class ModerationForm(forms.ModelForm):
    class Meta:
        model = Moderation
        fields = []


class HistoryForm(forms.ModelForm):
    class Meta:
        model = History
        fields = []


class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ["name"]


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["edits"]
