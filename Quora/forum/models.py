from django.db import models

from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver

from django.core.mail import send_mail
from django.conf import settings

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


class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, verbose_name='user', related_name='profile', on_delete=models.CASCADE)
    name = models.CharField(max_length = 30, blank=True, null=True)
    bio = models.TextField(max_length = 500, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    address = models.CharField(max_length = 200, blank=True, null=True)
    followers = models.ManyToManyField(User, blank = True, related_name='followers')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        print('created')
        UserProfile.objects.create(user=instance)

        subject = 'Welcome'
        message = 'Your profile was created successfully'
        email = 'kumar.shiv68@yahoo.com' # Email sending to

        send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
        )


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    print('\n saved')
    instance.profile.save()
