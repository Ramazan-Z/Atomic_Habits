from django.urls import path

from habits import views
from habits.apps import HabitsConfig

app_name = HabitsConfig.name

urlpatterns = [
    path("new_habit/", views.HabitNewView.as_view(), name="new-habit"),
]
