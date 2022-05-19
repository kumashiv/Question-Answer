from django.contrib import admin

from .models import Question, Comment, Like

# Register your models here.
admin.site.register(Question)
admin.site.register(Comment)
admin.site.register(Like)
