from django.contrib import admin

# Register your models here.
from common.models import  (Menu)

class MenuAdmin(admin.ModelAdmin):
    pass
admin.site.register(Menu, MenuAdmin)


# admin.register()

