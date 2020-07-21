from django.db import models

class Profile(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=50)
    profile = models.TextField()
    def __str__(self):
        return self.name