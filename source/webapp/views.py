from django.shortcuts import render, \
    get_object_or_404, redirect, reverse
from webapp.models import Exercise
from webapp.forms import ExerciseForm
from django.views.generic import TemplateView, \
    View, FormView
from webapp.base_views import FormView as \
    CustomFormView

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exercises'] = Exercise.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        for exercise_pk in request.POST.getlist('exercises', []):
            Exercise.objects.get(pk=exercise_pk).delete()
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class ExerciseView(TemplateView):
    template_name = 'exercise.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exercise'] = get_object_or_404(Exercise, pk=kwargs['pk'])
        return context

class ExerciseCreateView(CustomFormView):
    template_name = "create.html"
    form_class = ExerciseForm

    def get_redirect_url(self):
        return reverse('exercise_view',
                       kwargs={'pk':
                                   self.exercise.pk})

    def form_valid(self, form):
        self.exercise = form.save()
        return super().form_valid(form)

class ExerciseUpdateView(FormView):
    template_name = 'exercise_update.html'
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
        return render(request, 'exercise_delete.html', {'exercise': exercise})

    def post(self, request, *args, **kwargs):
        exercise = get_object_or_404(Exercise, pk=kwargs['pk'])
        exercise.delete()
        return redirect('index')


