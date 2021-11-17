import logging

from django.db import models
from django.urls import reverse

log = logging.getLogger(__name__)


class ImageLoad(models.Model):
    title = models.CharField(verbose_name='Название', max_length=300, blank=True, )
    image = models.ImageField(verbose_name='Файл', blank=True, upload_to='images')

    def __str__(self):
        return self.title

    def get_absolute_url(self, *args, **kwargs):
        return reverse('image-view', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        self.title = self.image.name
        return super().save(*args, **kwargs)
