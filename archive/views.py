from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView

from .models import ToolInstance


class ArchiveDashboardView(LoginRequiredMixin, ListView):
    model = ToolInstance
    template_name = 'archive/dashboard.html'
    context_object_name = 'records'
    paginate_by = 10

    def get_queryset(self):
        return ToolInstance.objects.filter(
            user=self.request.user,
            status='archived',
        ).order_by('-submitted_at')


class ArchiveDetailView(LoginRequiredMixin, DetailView):
    model = ToolInstance
    template_name = 'archive/detail.html'
    context_object_name = 'record'

    def get_queryset(self):
        return ToolInstance.objects.filter(user=self.request.user)
