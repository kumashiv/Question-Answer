from django.contrib import admin

from .models import Question, Comment, Like, UserProfile

# Register your models here.
admin.site.register(Question)
admin.site.register(Comment)
admin.site.register(Like)

admin.site.register(UserProfile)
