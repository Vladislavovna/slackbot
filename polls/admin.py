from django.contrib import admin

# Register your models here.
from .models import Poll, Question, PollSchedule, SlackUser, PollAnswer, QuestionAnswer

admin.site.register(Question)
admin.site.register(PollSchedule)
admin.site.register(SlackUser)


class QuestionInline(admin.TabularInline):
    model = Question


class QuestionAnswerInline(admin.TabularInline):
    model = QuestionAnswer


class PollAdmin(admin.ModelAdmin):
    inlines = [
        QuestionInline
    ]


class PollAnswerAdmin(admin.ModelAdmin):
    inlines = [
        QuestionAnswerInline
    ]
    search_fields = (
        'poll__name',
    )
    list_filter = ('poll__name', 'slack_user__username')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(Poll, PollAdmin)
admin.site.register(PollAnswer, PollAnswerAdmin)
