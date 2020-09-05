from django.contrib import admin

# Register your models here.
from .models import *

# admin.site.register(User)


class UserAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['id', 'username', 'stuid', 'stuname', 'role', ]
    search_fields = ['stuname', 'stuid', ]
    # list_editable =
    list_filter = ['role', ]
    ordering = ['stuid']


admin.site.register(User, UserAdmin)