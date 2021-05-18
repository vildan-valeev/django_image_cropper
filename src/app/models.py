from django.db import models
from django.urls import reverse


class Img(models.Model):

    image = models.ImageField(verbose_name='Файл', )

    def __str__(self):
        return str(self.image)

    def get_absolute_url(self, *args, **kwargs):
        return reverse('image-view', kwargs={'pk': self.pk})