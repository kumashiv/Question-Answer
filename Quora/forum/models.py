from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length = 200)
    pub_date = models.DateTimeField(auto_now_add = True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.question_text

class Comment(models.Model):
    comment_text = models.CharField(max_length = 1000)
    pub_date = models.DateTimeField(auto_now_add = True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    def __str__(self):
        return self.comment_text

class Like(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
