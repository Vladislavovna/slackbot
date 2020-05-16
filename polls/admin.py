from django.contrib import admin

# Register your models here.
from .models import Poll, Question, PollSchedule, SlackUser

admin.site.register(Question)
admin.site.register(PollSchedule)
admin.site.register(SlackUser)


class QuestionInline(admin.TabularInline):
    model = Question


class PollAdmin(admin.ModelAdmin):
    inlines = [
        QuestionInline
    ]


admin.site.register(Poll, PollAdmin)
