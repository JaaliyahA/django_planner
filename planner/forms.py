from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm, TextInput, EmailInput, Textarea, Select,BooleanField ,DateInput, RadioSelect
from .models import Task, Note, User, ToDoList

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