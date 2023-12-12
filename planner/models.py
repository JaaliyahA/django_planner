from django.db import models
from django.contrib.auth.models import AbstractUser
# class Monthly(models.Model):
#     name = models.CharField(max_length=30)

class User(AbstractUser):
    avatar = models.ImageField(default="https://static.vecteezy.com/system/resources/thumbnails/009/734/564/small/default-avatar-profile-icon-of-social-media-user-vector.jpg", upload_to="user_images")
    bio = models.TextField()


class ToDoList(models.Model):
    title = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.title}"

# class Daily(models.Model):
#     day = models.DateField(auto_now = False)
#     todolist = models.ManyToManyField(ToDoList, related_name="daily")

#     def __str__(self):
#         return f"{self.day}"
#     class Meta:
#         verbose_name_plural = "Dailies"

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now = True)
    due_date = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Tasks" )
    is_completed = models.BooleanField(default=False)
    todolist = models.ForeignKey(ToDoList, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}: due {self.due_date}"
    
    class Meta:
        ordering = ["due_date"]

class Note(models.Model):
    title = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Notes" )
    is_important = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title}'
