from django.db import models

class User(models.Model):
    name = models.CharField(max_length=25, unique=True)
    codechef = models.CharField(max_length=25, blank=True, unique=True)
    spoj = models.CharField(max_length=25, blank=True, unique=True)
    codeforce = models.CharField(max_length=25, blank=True, unique=True)
    last_sync = models.DateField(null=True, blank=True)
    totalCC = models.IntegerField(default=0)
    totalSJ = models.IntegerField(default=0)
    totalCF = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Sj(models.Model):
    handle = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return self.handle.name

class Cc(models.Model):
    handle = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return self.handle.name

class Cf(models.Model):
    handle = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return self.handle.name