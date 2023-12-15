from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm, TextInput, EmailInput, Textarea, Select ,DateInput, FileInput
from .models import Task, Note, User, ToDoList

class UserForm(forms.ModelForm):
    class Meta:
        model= User
        fields = ("email", "avatar", "bio")
        widgets = {
            "email": EmailInput(attrs={
                'class': "form-control mb-3",
                'style': 'max-width: 500px;',
                'placeholder': ''
            }),
             "bio": Textarea(attrs={
                'class': "form-control mb-3",
                'style': 'max-width: 500px;',
                'placeholder': 'Bio'
            }),
             "avatar": FileInput(attrs={
                'class': "form-control mb-3",
                'style': 'max-width: 500px;',
                
            }),
        }

class DateInput(forms.DateInput):
    input_type = 'date'

class TaskForm(forms.ModelForm):
    class Meta:
        model= Task
        fields = ("title", 'description', "due_date", "todolist")
        labels = {
            'due_date': "When is this due?",
        }
        widgets = {
            "title": TextInput(attrs={
                'class': "form-control mb-3",
                'style': 'max-width: 500px;',
                'placeholder': ''
                }),
            "description": Textarea(attrs={
                'class': "form-control mb-3",
                'style': 'max-width: 500px;',
                'placeholder': 'Description'
            }),
            "due_date": DateInput(attrs={
                "class": "form-control mb-3",
                "style": 'max-width: 500px;',
            }),
            "todolist": Select(attrs={
                "class": "form-select mb-3",
                "style":'max-width: 500px;',
            })
        }

class NoteForm(forms.ModelForm):

    
    class Meta:
        model = Note
        fields = ("title", "is_important")
        labels = {
            "is_important": "Mark as Important?"
        }
        widgets = {
            "title": TextInput(attrs={
                'class': "form-control mb-3",
                'style': 'max-width: 500px;',
                'placeholder': ''
                }),
            "is_important": Select(attrs={
                "class": "form-select mb-3",
                "style":'max-width: 500px;',
            }, choices=((True, "Yes"), (False, "No")))
        }