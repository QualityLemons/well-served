from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, LogoutView

from .forms import CustomUserCreationForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'registration/signup.html'


class UserLoginView(LoginView):
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
