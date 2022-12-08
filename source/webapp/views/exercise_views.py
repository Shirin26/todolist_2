from django.db.models import Q
from django.utils.http import urlencode
from django.shortcuts import render, \
    get_object_or_404, redirect, reverse
from webapp.models import Exercise, Project
from webapp.forms import ExerciseForm, SimpleSearchForm
from django.views.generic import TemplateView, \
    View, ListView, CreateView, UpdateView, DeleteView

class IndexView(ListView):
    template_name = 'exercise/index.html'
    context_object_name = 'exercises'
    model = Exercise
    ordering = ('-created_at',)
    paginate_by = 10
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
            return self.form.cleaned_data['search']

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            queryset = queryset.filter(Q(title__icontains=self.search_value) | Q(description__icontains=self.search_value))
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(
            object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
            context['search'] = self.search_value
        return context


class ExerciseView(TemplateView):
    template_name = 'exercise/exercise_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exercise'] = get_object_or_404(Exercise, pk=kwargs['pk'])
        return context


class ProjectExerciseCreateView(CreateView):
    template_name = 'exercise/create.html'
    model = Exercise
    form_class = ExerciseForm

    def get_success_url(self):
        return reverse('project_view', kwargs={
            'pk': self.object.project.pk})

    def form_valid(self, form):
        project = get_object_or_404(Project,
                                    pk=self.kwargs.get('pk'))
        form.instance.project = project
        return super().form_valid(form)


class ExerciseUpdateView(UpdateView):
    model = Exercise
    template_name = 'exercise/exercise_update.html'
    form_class = ExerciseForm
    context_object_name = 'exercise'

    def get_success_url(self):
        return reverse('project_view', kwargs={
            'pk': self.object.project.pk})


class ExerciseDeleteView(DeleteView):
    model = Exercise

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('project_view', kwargs={
            'pk': self.object.project.pk})

