from django.db import models


class Img(models.Model):
    image = models.ImageField(verbose_name='Изображения')

    def __str__(self):
        return str(self.id)
