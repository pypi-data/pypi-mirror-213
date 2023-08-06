from django.contrib import admin
from . import models
# Register your models here.

class HScodeAdmin(admin.ModelAdmin):
    list_display = [f.name for f in models.HScode._meta.fields]
    search_fields = [f.name for f in models.HScode._meta.fields]
    list_filter = ['hscode2']
admin.site.register(models.HScode, HScodeAdmin)