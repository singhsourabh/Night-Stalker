from django.contrib import admin
from . import models

admin.site.register(models.User)
admin.site.register(models.Sj)
admin.site.register(models.Cc)
admin.site.register(models.Cf)
