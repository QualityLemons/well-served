"""Authentication views for the accounts application.

Provides sign-up, login, and logout using Django's built-in class-based views
extended with project-specific configuration (email-only sign-up form,
authenticated-user redirect on the login page, and a fixed post-logout URL).
"""
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, LogoutView

from .forms import CustomUserCreationForm


class SignUpView(CreateView):
    """Registration form view.

    On successful submission Django creates the user and redirects to the
    login page so the new user can immediately sign in.
    """

    form_class = CustomUserCreationForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'registration/signup.html'


class UserLoginView(LoginView):
    """Email + password login form.

    ``redirect_authenticated_user`` sends already-logged-in visitors straight
    to their post-login destination instead of showing the form again.
    """

    template_name = 'registration/login.html'
    # Redirect already-authenticated users away from the login page so that
    # pressing the browser back button after login does not show the form again.
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    """Log the user out and send them to the login page.

    Overrides Django's default ``next_page`` (which is ``settings.LOGOUT_REDIRECT_URL``
    or the site root) so users always land on the login page after logging out.
    """

    next_page = reverse_lazy('accounts:login')
