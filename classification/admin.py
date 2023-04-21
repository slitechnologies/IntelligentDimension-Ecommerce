from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from . import models

# Register your models here.
class ClassificationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('class_name',)}
    list_display = ('class_name', 'slug')

admin.site.register(models.Classification, ClassificationAdmin)
