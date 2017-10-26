from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class kongtiao(models.Model):
    temperature = models.IntegerField('温度')

class light(models.Model):
    state = models.BooleanField('电灯状态')

    class Meta:
        db_table = 'light'


class house(models.Model):
    passCode = models.IntegerField('验证码',default='0')
    light = models.ManyToManyField(light)
    kongtiao = models.ManyToManyField(kongtiao)

    @classmethod
    def create(cls, passCode):
        house = cls(passCode=passCode)
        # do something with the book
        return house

    class Meta:
        db_table = 'house'


class houseUser(AbstractUser):
    role = models.CharField('家庭角色',max_length=50)
    birthday = models.DateField('生日')
    house = models.ForeignKey(house)

    class Meta:
        db_table = "houseUser"

        def __str__(self):
            return self.username





