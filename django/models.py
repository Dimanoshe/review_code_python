from django.contrib.auth.models import User
from django.db import models


class UserInfo(models.Model):
    # Каждая строка UserInfo соответствует только одной строке User
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        primary_key=True)
    inn = models.IntegerField(verbose_name='ИНН')
    account = models.FloatField(verbose_name='Счёт')

    def __str__(self):
        return '{id} {inn}'.format(id=str(self.id), inn=self.inn)
