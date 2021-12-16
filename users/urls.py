from django.urls import path

from users.views import (
    registration_view,
    logout_view,
    demo_user_login_view,
    UserUpdateView,
    UserCreateView,
    UserDeleteView,
    UserDetailView
)

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', registration_view, name='register'),
    path('user-create/', UserCreateView.as_view(), name='user_create'),
    path('user-delete/<slug:slug>/', UserDeleteView.as_view(), name='user_delete'),

    path('login/',
         auth_views.LoginView.as_view(template_name='users/login.html', redirect_authenticated_user=True),
         name='login'),
    path('demo_login/', demo_user_login_view, name='demo_login'),
    path('logout/', logout_view, name='logout'),

    path('user-update/<slug:slug>/', UserUpdateView.as_view(), name='user_update'),
    path('user-profile/<slug:slug>/', UserDetailView.as_view(), name='user_profile'),

    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'), name='password_reset_complete'),
]
