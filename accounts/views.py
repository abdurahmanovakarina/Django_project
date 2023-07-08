from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from wiki.models import Article
from .forms import (
    CustomUserCreationForm,
    UpdateProfileForm,
    CustomUserUpdateForm,
    CommentForm,
)
from .models import CustomUser, Comment


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class UpdateUserView(UpdateView):
    form_class = CustomUserUpdateForm
    success_url = reverse_lazy("home")
    template_name = "registration/update_user.html"

    def get_object(self, **kwargs):
        return self.request.user


class UpdateProfileView(UpdateView):
    model = CustomUser
    form_class = UpdateProfileForm
    success_url = reverse_lazy("profile")
    template_name = "registration/update_profile.html"

    def get_object(self, **kwargs):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy("profile", kwargs={"username": self.request.user.username})


def delete_profile_picture(request):
    if request.method == "POST":
        user = CustomUser.objects.get(pk=request.user.id)
        if user.profile_picture:
            user.profile_picture.delete()
            user.save()
            return JsonResponse({"success": True})
        else:
            return JsonResponse(
                {"success": False, "error": "No profile picture found."}
            )
    else:
        return JsonResponse({"success": False, "error": "Invalid request method."})


@login_required
def profile(request, username):
    user = get_object_or_404(CustomUser, username=username)
    form = CommentForm(request.POST or None)
    is_owner = False
    if request.user.username == username:
        is_owner = True
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.profile = user
        comment.save()
        messages.success(request, "Comment added successfully.")
        return redirect("profile", username=username)
    comments = Comment.objects.filter(profile=user)
    articles_count = Article.objects.filter(created_by=user).count()
    paginator = Paginator(comments, 10)  # показывать 10 комментариев на странице
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "registration/profile.html",
        {
            "form": form,
            "user": user,
            "page_obj": page_obj,
            "is_owner": is_owner,
            "articles_count": articles_count,
        },
    )


def user_list(request):
    users = CustomUser.objects.all()

    # Handle filtering logic if necessary
    # ...

    paginator = Paginator(users, 10)  # Display 10 users per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "registration/user_list.html", {"page_obj": page_obj})
