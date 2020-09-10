from django.contrib import admin

# Register your models here.
from backend.models import *

# admin.site.register(User)


class UserAdmin(admin.ModelAdmin):
    list_per_page = 30
    list_display = ['id', 'username', 'stuid', 'stuname', 'role', ]
    search_fields = ['stuname', 'stuid', ]
    # list_editable =
    list_filter = ['role', ]
    ordering = ['stuid']


class HomeWorkAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['id', 'title', 'homeworktype', 'author', ]
    list_filter = ['homeworktype', ]


class GroupAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['id', 'grouptype', 'leader', ]
    list_filter = ['grouptype', 'leader', ]


class JudgementAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['id', 'student', 'group', 'judger', ]
    list_filter = ['judger', ]


admin.site.register(User, UserAdmin)
admin.site.register(HomeWork, HomeWorkAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Judgement, JudgementAdmin)
