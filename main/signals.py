from django.core.signals import request_started, request_finished
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils import timezone


from main import models


@receiver(user_logged_in)
def on_login(sender, request, user, **kwargs):
    activity_obj = models.UserActivity.objects.filter(user=user).first()
    activity_obj.login_date = timezone.now()
    activity_obj.save()


@receiver(post_save, sender='auth.User')
def on_create_user(sender, instance, created, **kwargs):
    if created:
        models.UserActivity.objects.create(
            user=instance
        )