from django.db import models
from django.utils import timezone


class Ingredient(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    chef = models.ForeignKey('auth.User')
    created_date = models.DateTimeField(default=timezone.now)
    standard = models.BooleanField(default=False)
    ingredients = models.ManyToManyField('Ingredient')

    def __str__(self):
        return self.name

def thirty_day():
    return timezone.now() + timezone.timedelta(days=30)

class Menu(models.Model):
    season = models.CharField(max_length=20)
    items = models.ManyToManyField('Item', related_name='items')
    created_date = models.DateTimeField(default=timezone.now)
    expiration_date = models.DateTimeField(null=False, default=thirty_day)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.season
