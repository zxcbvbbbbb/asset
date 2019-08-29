from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.User)
admin.site.register(models.Role)
admin.site.register(models.User2Role)
admin.site.register(models.Permission)
admin.site.register(models.Action)
admin.site.register(models.Permission2Action)
admin.site.register(models.Permission2Action2Role)
admin.site.register(models.Menu)
admin.site.register(models.Models)
admin.site.register(models.Type)
admin.site.register(models.Department)
admin.site.register(models.Employee)
admin.site.register(models.Configuration)
admin.site.register(models.Classes)
admin.site.register(models.Student)
admin.site.register(models.Teacher)

class AssetDisplay(admin.ModelAdmin):
    list_display = ['id','name','mod','price','recipient','sn','supplier','after_sales','status']

admin.site.register(models.Asset,AssetDisplay)



