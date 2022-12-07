from django.db.models import Q
from django.utils.http import urlencode
from django.shortcuts import render, \
    get_object_or_404, redirect, reverse
from webapp.models import Exercise, Project
from webapp.forms import ExerciseForm, SimpleSearchForm
from django.views.generic import TemplateView, \
    View, FormView, ListView, CreateView

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
    template_name = 'exercise/exercise.html'

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


class ExerciseUpdateView(FormView):
    template_name = 'exercise/exercise_update.html'
    form_class = ExerciseForm

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Exercise, pk=pk)

    def dispatch(self, request, *args, **kwargs):
        self.exercise = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['exercise'] = self.exercise
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.exercise
        return kwargs

    def form_valid(self, form):
        self.exercise = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('exercise_view',
                       kwargs={'pk':
                                   self.exercise.pk})


class DeleteExercise(View):
    def get(self, request, *args, **kwargs):
        exercise = get_object_or_404(Exercise, pk=kwargs['pk'])
        return render(request,
                      'exercise/exercise_delete.html', {'exercise': exercise})

    def post(self, request, *args, **kwargs):
        exercise = get_object_or_404(Exercise, pk=kwargs['pk'])
        exercise.delete()
        return redirect('index')


