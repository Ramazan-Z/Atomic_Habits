from django.contrib import admin

from habits.models import Habit, MomentHabit


@admin.register(MomentHabit)
class MomentHabitAdmin(admin.ModelAdmin):

    list_display = ("id", "time", "title")
    search_fields = ("title",)


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):

    list_display = ("id", "action")
    list_filter = ("is_pleasant", "is_public")
    search_fields = ("action", "place")
