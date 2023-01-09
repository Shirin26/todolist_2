from django.urls import reverse_lazy
from django.shortcuts import redirect
from webapp.models import Project
from django.views.generic import ListView, \
    DetailView, CreateView, UpdateView, DeleteView
from webapp.forms import SimpleSearchForm, \
    ProjectForm, ChangeUsersForm
from django.utils.http import urlencode
from django.db.models import Q
from django.contrib.auth.mixins import PermissionRequiredMixin


class IndexProjectViews(ListView):
    template_name = 'project/index_project.html'
    context_object_name = 'projects'
    model = Project
    paginate_by = 2
    paginate_orphans = 2

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
        return queryset.filter(
            is_deleted=False).order_by('-start_date')


class ProjectView(DetailView):
    template_name = 'project/project_view.html'
    model = Project
    queryset = Project.objects.filter(
        is_deleted=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object
        exercises = project.exercises.order_by(
            '-created_at')
        context['exercises'] = exercises
        return context


class ProjectCreateView(PermissionRequiredMixin,
                        CreateView):
    template_name = 'project/project_create.html'
    model = Project
    form_class = ProjectForm
    permission_required = 'webapp.add_project'

    def form_valid(self, form):
        self.object = form.save()
        self.object.users.add(self.request.user)
        return super().form_valid(form)

class ProjectUpdateView(PermissionRequiredMixin,
                        UpdateView):
    template_name = 'project/project_update.html'
    form_class = ProjectForm
    model = Project
    context_object_name = 'project'
    permission_required = 'webapp.change_project'


class ProjectDeleteView(PermissionRequiredMixin,
                        DeleteView):
    template_name = 'project/project_delete.html'
    model = Project
    context_object_name = 'project'
    success_url = reverse_lazy(
        'webapp:exercise_project_index')
    permission_required = 'webapp.delete_project'

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.is_deleted = True
        self.object.save()
        return redirect(success_url)


class ChangeUsersView(PermissionRequiredMixin,
                      UpdateView):
    model = Project
    form_class = ChangeUsersForm
    template_name = 'project/change_user.html'
    permission_required = 'webapp.add_user_in_project'
    
    def has_permission(self):
        return super().has_permission() and \
            self.request.user in \
            self.get_object().users.all()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs