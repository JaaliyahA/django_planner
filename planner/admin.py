from django.contrib import admin
from planner.models import  ToDoList, User, Task, Note
# Register your models here.


admin.site.register(ToDoList)
admin.site.register(User)
admin.site.register(Task)
admin.site.register(Note)