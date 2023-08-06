from django.contrib import admin
from . import models
# Register your models here.

class AreaAdmin(admin.ModelAdmin):
    list_display = [f.name for f in models.Area._meta.fields]
    search_fields = [f.name for f in models.Area._meta.fields]
    list_filter = ['zone']
admin.site.register(models.Area, AreaAdmin)