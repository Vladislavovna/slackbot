from django.contrib import admin

# Register your models here.
from .models import Poll, Question

admin.site.register(Poll)
admin.site.register(Question)

