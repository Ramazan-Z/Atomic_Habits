from django.urls import path

from habits import views
from habits.apps import HabitsConfig

app_name = HabitsConfig.name

urlpatterns = [
    path("new_habit/", views.HabitNewView.as_view(), name="new-habit"),
    path("my_habits/", views.MyHabitsView.as_view(), name="my-habits"),
    path("public_habits/", views.PublicHabitsView.as_view(), name="public-habits"),
    path("edit_habit/<int:pk>/", views.HabitEditView.as_view(), name="edit-habit"),
    path("retrieve_habit/<int:pk>/", views.HabitRetrieveView.as_view(), name="retrieve-habit"),
    path("destroy_habit/<int:pk>/", views.HabitDestroyView.as_view(), name="destroy-habit"),
]
