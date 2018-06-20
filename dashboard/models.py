from django.db import models

class User(models.Model):
    name = models.CharField(max_length=25, unique=True)
    codechef = models.CharField(max_length=25, blank=True)
    spoj = models.CharField(max_length=25, blank=True)
    codeforce = models.CharField(max_length=25, blank=True)
    last_sync = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name