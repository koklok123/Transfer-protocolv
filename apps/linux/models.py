from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    balance = models.PositiveIntegerField(default=4, null=False)  # Начальный баланс
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    wallet = models.IntegerField(default=0)  # Кошелек пользователя

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
