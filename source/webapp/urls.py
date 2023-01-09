
from django.urls import path
from webapp.views import IndexView, \
    ExerciseView, ExerciseUpdateView, IndexProjectViews, \
    ProjectView, ProjectCreateView, \
    ProjectExerciseCreateView, \
    ProjectUpdateView, ProjectDeleteView, \
    ExerciseDeleteView, ChangeUsersView

app_name = 'webapp'

urlpatterns = [
    path('', IndexProjectViews.as_view(),
         name='exercise_project_index'),
    path('project/<int:pk>/',
         ProjectView.as_view(),
         name='project_view'),
    path('project/add/',
         ProjectCreateView.as_view(),
         name='project_add'),
    path('project/<int:pk>/update/',
         ProjectUpdateView.as_view(),
         name='project_update'),
    path('project/<int:pk>/delete/',
         ProjectDeleteView.as_view(),
         name='project_delete'),

    path('exercise/', IndexView.as_view(),
         name='index'),
    path('exercise/<int:pk>/', ExerciseView.as_view(), name='exercise_view'),
    path('project/<int:pk>/exercise/add/',
         ProjectExerciseCreateView.as_view(),
         name='project_exercise_add'),
    path('exercise/<int:pk>/update/',
         ExerciseUpdateView.as_view(), name='exercise_update'),
    path('exercise/<int:pk>/delete/',
         ExerciseDeleteView.as_view(), name='exercise_delete'),

    path('project/<int:pk>/change-users/',
         ChangeUsersView.as_view(),
         name='change_users'),
]