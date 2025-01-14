from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    '''Расширенаая модель User '''
    photo = models.ImageField(
        upload_to="user_photos/",
        blank=True,
        null=True,
        verbose_name="Фото профиля",
        default=None
    )
    groups = models.ManyToManyField(
        "auth.Group", related_name="clients_user_set", blank=True, verbose_name="groups"
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="clients_user_permissions_set",
        blank=True,
        verbose_name="user permissions",
    )

    date_birth = models.DateField(blank=True, null=True, verbose_name="Дата рождения")

class Subscription(models.Model):
    '''Модель подписки одного пользователя на другого'''
    subscriber = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="subscribers"
    )
    channel = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="channels"
    )
    subscribed_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        unique_together = ("subscriber", "channel")



