from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    """User creation form for the email-as-username model.

    Inherits from Django's built-in ``UserCreationForm`` but restricts the
    fields to ``email`` only — there is no username field on this model.
    """

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
    """User change form for the admin edit view.

    Mirrors ``CustomUserCreationForm``: exposes only the ``email`` field,
    matching the email-as-username model used throughout the project.
    """

    class Meta:
        model = User
        fields = ('email',)
