from django.db import models
from django.contrib.auth.models import User


class File(models.Model):
    file = models.FileField(upload_to='store/files/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.file.name


class Tag(models.Model):
    name = models.CharField(max_length=100)
    files = models.ManyToManyField(File)
