# App namespace: 'accounts'
# Named URLs exposed by this module:
#   accounts:signup  — user registration page
#   accounts:login   — login page (referenced by login_required redirects)
#   accounts:logout  — POST-only logout endpoint
from django.urls import path
from .views import SignUpView, UserLoginView, UserLogoutView

app_name = 'accounts'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]
