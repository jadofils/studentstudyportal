from django.db import models
from django.contrib.auth.models import User
from . models import *
from datetime import date, time
from django.contrib.auth.models import User




class Notes(models.Model):  # Updated to uppercase
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'note'
        verbose_name_plural = 'notes'

class Homework(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    description = models.TextField()
    due = models.DateTimeField()
    is_finished = models.BooleanField(default=False)  # Corrected the typo

    def __str__(self):
        return self.title



class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    is_finished = models.BooleanField(default=False)
    day = models.DateField(default=date.today)  # Default to today's date
    place = models.CharField(max_length=100, default='Unknown')  # Default value for new field
    time = models.TimeField(default=time(0, 0))  # Default to midnight

    def __str__(self):
        return f'{self.title} - {self.day} {self.time}'

    def get_formatted_datetime(self):
        return f'{self.day.strftime("%B %d, %Y")} at {self.time.strftime("%I:%M %p")}'
    

