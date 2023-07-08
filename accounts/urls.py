from django.urls import path

from accounts import views
from django.contrib.auth import views as auth_views
from accounts.views import SignUpView, UpdateUserView, UpdateProfileView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path(
        "password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path("update_user/", UpdateUserView.as_view(), name="update_user"),
    path("profile/update/", UpdateProfileView.as_view(), name="update_profile"),
    path(
        "profile/update/delete-profile-picture/",
        views.delete_profile_picture,
        name="delete_profile_picture",
    ),
    path("all/", views.user_list, name="society"),
    path("<str:username>/", views.profile, name="profile"),
]
