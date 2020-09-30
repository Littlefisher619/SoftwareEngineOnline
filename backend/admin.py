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
    list_display = ['id', 'get_stuname', 'get_stuid', 'get_groupname', 'judger', 'totalscore']
    list_filter = ['homework',]
    search_fields = ['student__stuname', 'group__groupname', 'student__stuid',]

    def get_stuname(self, judgement):
        return judgement.student.stuname if judgement.student else None

    get_stuname.short_description = '学生姓名'
    get_stuname.admin_order_field = 'student__stuname'

    def get_stuid(self, judgement):
        return judgement.student.stuid if judgement.student else None

    get_stuid.short_description = '学生学号'
    get_stuid.admin_order_field = 'student__stuid'

    def get_groupname(self, judgement):
        return judgement.group.groupname if judgement.group else None

    get_groupname.short_description = '组名'
    get_groupname.admin_order_field = 'group__groupname'




admin.site.register(User, UserAdmin)
admin.site.register(HomeWork, HomeWorkAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Judgement, JudgementAdmin)
