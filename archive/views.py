"""Views for the archive application.

Covers four areas:
- **Archive dashboard** (``ArchiveDashboardView``) — lists a user's solo
  archived submissions and the collaborative sessions they participated in.
- **Archive detail / delete** (``ArchiveDetailView``, ``archive_record_delete``)
  — shows a single submission and allows the owner to delete it.
- **Waiting list** (``waiting_list_signup``) — public page that collects email
  addresses; deduplicates by email using ``get_or_create``.
- **Feature requests** (``feature_request``) — public page that stores
  free-text feature ideas with an optional contact email.
"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView

from .models import ToolInstance, ToolSession, WaitingListEntry


class ArchiveDashboardView(LoginRequiredMixin, ListView):
    """Paginated list of the user's solo archived submissions.

    Also injects a ``sessions`` queryset (sessions the user hosted or
    participated in) and, for staff users, the full waiting-list table.
    """

    model = ToolInstance
    template_name = 'archive/dashboard.html'
    context_object_name = 'records'
    paginate_by = 10

    def get_queryset(self):
        return ToolInstance.objects.filter(
            user=self.request.user,
            status='archived',
            # Solo submissions only — instances that belong to a session
            # are shown in the sessions table below, not in this list.
            session__isnull=True,
        ).order_by('-submitted_at')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        # Q(host=user) | Q(instances__user=user) returns sessions this user
        # hosted OR participated in as a contributor.  distinct() prevents
        # duplicate rows caused by the JOIN when a user has multiple instances
        # in the same session.
        ctx['sessions'] = (
            ToolSession.objects
            .filter(Q(host=user) | Q(instances__user=user))
            .distinct()
            .order_by('-created_at')[:25]
        )
        ctx['user'] = user
        if user.is_staff:
            ctx['waiting_list'] = WaitingListEntry.objects.all()
            ctx['waiting_list_count'] = WaitingListEntry.objects.count()
        return ctx


class ArchiveDetailView(LoginRequiredMixin, DetailView):
    """Detail view for a single ``ToolInstance`` record.

    The queryset is scoped to ``user=request.user`` so users cannot access
    each other's records by guessing or manipulating the primary key.
    """

    model = ToolInstance
    template_name = 'archive/detail.html'
    context_object_name = 'record'

    def get_queryset(self):
        return ToolInstance.objects.filter(user=self.request.user)


@login_required
# @require_POST prevents accidental deletion triggered by a browser that
# prefetches the URL as a GET request (e.g. from a link hover or <link rel=prefetch>).
@require_POST
def archive_record_delete(request, pk):
    instance = get_object_or_404(ToolInstance, pk=pk, user=request.user)
    instance.delete()
    messages.success(request, 'Record deleted successfully.')
    return redirect('archive:dashboard')


def waiting_list_signup(request):
    """Public page — collect email addresses for the waiting list."""
    from django import forms as django_forms

    # Defined inside the view because it is used only here.
    # A module-level class would pollute the forms namespace without benefit.
    class WaitingListForm(django_forms.Form):
        name = django_forms.CharField(
            label='Your name (optional)', max_length=200, required=False,
            widget=django_forms.TextInput(attrs={'placeholder': 'e.g. Sarah'}),
        )
        email = django_forms.EmailField(
            label='Your email address',
            widget=django_forms.EmailInput(attrs={'placeholder': 'you@example.com'}),
        )

    success = False
    already_on_list = False
    form = WaitingListForm()

    if request.method == 'POST':
        form = WaitingListForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].lower().strip()
            name = form.cleaned_data.get('name', '').strip()
            try:
                _entry, created = WaitingListEntry.objects.get_or_create(
                    email=email,
                    defaults={'name': name},
                )
                success = True
                already_on_list = not created
                form = WaitingListForm()
            except Exception:
                messages.error(
                    request,
                    'Something went wrong on our end — please try again.',
                )

    return render(request, 'archive/waiting_list_signup.html', {
        'form': form,
        'success': success,
        'already_on_list': already_on_list,
    })


def feature_request(request):
    """Public page — collect feature requests."""
    from django import forms as django_forms

    # Defined inside the view because it is used only here.
    # A module-level class would pollute the forms namespace without benefit.
    class FeatureRequestForm(django_forms.Form):
        name = django_forms.CharField(
            label='Your name (optional)', max_length=200, required=False,
            widget=django_forms.TextInput(attrs={'placeholder': 'e.g. Sarah'}),
        )
        email = django_forms.EmailField(
            label='Your email (optional)',
            required=False,
            widget=django_forms.EmailInput(attrs={'placeholder': 'you@example.com'}),
            help_text="We'll only use this to let you know when the feature ships.",
        )
        title = django_forms.CharField(
            label='Feature title',
            max_length=300,
            widget=django_forms.TextInput(attrs={
                'placeholder': 'e.g. Export session results as PDF',
            }),
        )
        description = django_forms.CharField(
            label='Tell us more',
            widget=django_forms.Textarea(attrs={
                'rows': 5,
                'placeholder': (
                    'What problem would this solve? '
                    'How do you imagine it working?'
                ),
            }),
        )

    success = False
    form = FeatureRequestForm()

    if request.method == 'POST':
        form = FeatureRequestForm(request.POST)
        if form.is_valid():
            from .models import FeatureRequest
            try:
                FeatureRequest.objects.create(
                    name=form.cleaned_data.get('name', '').strip(),
                    email=form.cleaned_data.get('email', '').strip().lower(),
                    title=form.cleaned_data['title'].strip(),
                    description=form.cleaned_data['description'].strip(),
                )
                success = True
                form = FeatureRequestForm()
            except Exception:
                messages.error(
                    request,
                    'Something went wrong on our end — please try again.',
                )

    return render(request, 'archive/feature_request.html', {
        'form': form,
        'success': success,
    })
