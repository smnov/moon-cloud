from django.db import models
from django.contrib.auth.models import User


class File(models.Model):
    file = models.FileField(upload_to='store/files/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

    @property
    def file_size(self):
        size = self.file.size
        max_size = 512000
        if size < max_size:
            value = round(size/1000,2)
            ext = ' kb'
        elif size < max_size * 1000:
            value = round(size / 1000000,2)
            ext = ' mb'
        else:
            value = round(size/1000000000,2)
            ext = ' gb'
        return str(value)+ext