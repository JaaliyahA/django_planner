from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    re_path(r'^calendar/$', views.CalendarView.as_view(), name="calendar"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("<int:year>/<int:month>/<int:day>", views.daily, name="daily"),
    path("tasks", views.taskList, name="taskList"),
    path("notes", views.noteList, name="noteList"),
    path("profile/", views.profile, name="profile"),
    path("new_task", views.create_new, name="new_task"),
    path("new_note", views.new_note, name="new_note"),


]