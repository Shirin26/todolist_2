from webapp.models import Project
from django.views.generic import ListView, DetailView
from webapp.forms import SimpleSearchForm
from django.utils.http import urlencode
from django.db.models import Q

class IndexProjectViews(ListView):
    template_name = 'project/index_project.html'
    context_object_name = 'projects'
    model = Project
    ordering = ('-start_date')

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args,
                           **kwargs)

    def get_search_form(self):
        return SimpleSearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data[
                'search']
        return None

    def get_context_data(self, *,
                         object_list=None,
                         **kwargs):
        context = super().get_context_data(
            object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({
                'search': self.search_value})
            context['search'] = self.search_value
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            queryset = queryset.filter(
                Q(
                    name__icontains=self.search_value) | Q(
                    project_description__icontains=self.search_value))
        return queryset


class ProjectView(DetailView):
    template_name = 'project/project_view.html'
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object
        exercises = project.exercises.order_by(
            '-created_at')
        context['exercises'] = exercises
        return context
