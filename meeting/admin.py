from django.contrib import admin

from .models import Interview, Interviewee, Interviewer


models_list = [Interview, Interviewee, Interviewer]
admin.site.register(models_list)
