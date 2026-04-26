from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import ToolInstance, ToolSession, WaitingListEntry


class ArchiveDashboardView(LoginRequiredMixin, ListView):
    model = ToolInstance
    template_name = 'archive/dashboard.html'
    context_object_name = 'records'
    paginate_by = 10

    def get_queryset(self):
        return ToolInstance.objects.filter(
            user=self.request.user,
            status='archived',
            session__isnull=True,
        ).order_by('-submitted_at')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
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
    model = ToolInstance
    template_name = 'archive/detail.html'
    context_object_name = 'record'

    def get_queryset(self):
        return ToolInstance.objects.filter(user=self.request.user)


def waiting_list_signup(request):
    """Public page — collect email addresses for the waiting list."""
    from django import forms as django_forms

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
            _entry, created = WaitingListEntry.objects.get_or_create(
                email=email,
                defaults={'name': name},
            )
            success = True
            already_on_list = not created
            form = WaitingListForm()

    return render(request, 'archive/waiting_list_signup.html', {
        'form': form,
        'success': success,
        'already_on_list': already_on_list,
    })


def feature_request(request):
    """Public page — collect feature requests."""
    from django import forms as django_forms

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
            FeatureRequest.objects.create(
                name=form.cleaned_data.get('name', '').strip(),
                email=form.cleaned_data.get('email', '').strip().lower(),
                title=form.cleaned_data['title'].strip(),
                description=form.cleaned_data['description'].strip(),
            )
            success = True
            form = FeatureRequestForm()

    return render(request, 'archive/feature_request.html', {
        'form': form,
        'success': success,
    })
