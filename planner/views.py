from django.shortcuts import render, redirect
from django.views.generic import ListView
import calendar
from .utils import Calendar
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms  import TaskForm, NoteForm, UserForm
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import User, ToDoList, Task, Note

class CalendarView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'planner/calendar.html'
    login_url = "/login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # use today's date for the calendar
        d = get_date(self.request.GET.get('month', None))
        print(d)
        
        cal = Calendar(d.year, d.month, user)

        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['date'] = f'{MONTHS[d.month - 1]} {d.year}'
        
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        context['prev_year'] = prev_year(d)
        context['next_year'] = next_year(d)
        return context
    
class SearchResultsView(ListView):
    model = Task
    template_name = 'planner/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = Task.objects.filter(
            Q(description__icontains=query) | Q(title__icontains=query)
        )
        return object_list
    
def prev_month(d):
        first = d.replace(day=1)
        prev_month = first - datetime.timedelta(days=1)
        month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
        return month
    
def next_month(d):
        days_in_month = calendar.monthrange(d.year, d.month)[1]
        last = d.replace(day=days_in_month)
        next_month = last + datetime.timedelta(days=1)
        month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
        return month
def prev_year(d):
        first = d.replace(day=1)
        prev_year = first - datetime.timedelta(days=365)
        print(prev_year)
        month = 'month=' + str(prev_year.year) + '-' + str(prev_year.month)
        return month
def next_year(d):
        first = d.replace(day=1)
        next_year = first + datetime.timedelta(days=365)
        month = 'month=' + str(next_year.year) + '-' + str(next_year.month)
        return month

def get_date(req_day):
        if req_day:
            year, month = (int(x) for x in req_day.split('-'))
            return datetime.date(year, month, day=1)
        return datetime.date.today()

MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

@login_required
def daily(request, year, month, day):
    date = f'{MONTHS[month-1]} {day}, {year}'
    in_progress_tasks = Task.objects.filter(is_completed = False,
                                            user = request.user)
    tasks = Task.objects.filter(due_date__day=day,
                                due_date__month=month,
                                due_date__year = year,
                                user = request.user)
    notes = Note.objects.filter(created_on__day=day, 
                                created_on__month = month,
                                created_on__year = year)
    return render(request, "planner/day.html", {"date":date, "tasks": tasks, "notes": notes, "in_prog_tasks": in_progress_tasks })

def index(request):
    return render(request, "planner/index.html")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("calendar"))
        else:
            return render(request, "planner/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "planner/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "planner/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "planner/register.html")
    
def taskList(request):
    taskList = Task.objects.all()

    return render(request, "planner/tasks.html", {"tasks":taskList})

def noteList(request):
    noteList = Note.objects.all()
    return render(request, "planner/notes.html", {"notes":noteList})

@login_required
def profile(request):
    return render(request, "planner/profile.html")

@login_required(login_url="login")
def create_new(request):
    if request.method == "POST":
        if "cancel" in request.POST:
            return redirect("index")
        form = TaskForm(request.POST)
        task = form.save(commit=False)
        task.user = request.user
        task.save()
        form.save_m2m()
        return redirect("index")
    else:
        form = TaskForm()
    return render(request, "planner/new_task.html", {"form":form})

@login_required(login_url="login")
def new_note(request):
    if request.method == "POST":
        if "cancel" in request.POST:
            return redirect("index")
        form = NoteForm(request.POST)
        note = form.save(commit=False)
        note.user = request.user
        note.save()
        form.save_m2m()
        return redirect("calendar")
    else:
        form = NoteForm()
    return render(request, "planner/new_note.html", {"form":form})

@login_required(login_url="login")
def edit_profile(request):
    profile = request.user
    if request.method == "POST":
        if "cancel" in request.POST:
            return redirect("profile")
        form = UserForm(request.POST, request.FILES, instance=profile)
        form.save()
        return redirect("profile")
    else:
        form = UserForm(instance=profile)
    return render(request, "planner/edit_profile.html", {"form":form})

