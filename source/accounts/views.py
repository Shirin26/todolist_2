from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, \
    login, logout
from accounts.forms import MyUserCreationForm
from django.views.generic import CreateView
from django.contrib.auth.models import User


class RegisterView(CreateView):
    model = User
    form_class = MyUserCreationForm
    template_name = 'user_create.html'


    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url

        next_url = self.request.POST.get('next')
        if next_url:
            return next_url

        return reverse('webapp:exercise_project_index')

def login_view(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('webapp:exercise_project_index')
        else:
            context['has_error'] = True
    return render(request, 'login.html', context=context)


def logout_view(request):
    logout(request)
    return redirect('webapp:exercise_project_index')







