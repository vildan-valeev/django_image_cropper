import os
from io import BytesIO
from urllib.request import urlopen

from PIL import Image
from django.core.exceptions import ValidationError
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.temp import NamedTemporaryFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.urls import reverse


class ImageLoad(models.Model):
    title = models.CharField(verbose_name='Название', max_length=300, blank=True, )
    image = models.ImageField(verbose_name='Файл', blank=True, )
    image_link = models.URLField(verbose_name='Ссылка', blank=True, null=True, )
    image_resized = models.ImageField(verbose_name='Измененный файл', blank=True, null=True, )
    width = models.PositiveIntegerField(verbose_name='Ширина', blank=True, null=True, )
    height = models.PositiveIntegerField(verbose_name='Высота', blank=True, null=True, )

    def __str__(self):
        return self.title

    def clean(self):
        if self.width and self.height:
            if int(self.width) >= 2000 or int(self.height) >= 2000:
                raise ValidationError('Превышен максимальный размер!')
            size = self.sizing(self.image.width, self.image.height)

            if round((self.width / size[0]), 1) != round((self.height / size[1]), 1):
                raise ValidationError(f'Укажите в пропорциях {self.image.width}x{self.image.height}. Или укажите только'
                                      f' одно из значений')

    def get_absolute_url(self, *args, **kwargs):
        return reverse('image-view', kwargs={'pk': self.pk})

    def sizing(self, width=None, height=None) -> tuple:
        size = None
        if width:
            width_percent = width / float(self.image.width)
            height_size = int((float(self.image.height) * float(width_percent)))
            size = (width, height_size)
        if height:
            height_percent = height / float(self.image.height)
            width_size = int((float(self.image.width) * float(height_percent)))
            size = (width_size, height)
        return size

    def save(self, *args, **kwargs):

        if (self.width and self.height) or self.width or self.height:
            original_name, original_ext = os.path.splitext(self.image.name)
            out_name = f'{original_name}_resized{original_ext}'
            im = Image.open(self.image.open())
            new_im = im.resize(size=self.sizing(self.width, self.height))
            buffer = BytesIO()
            self.image_resized.delete(save=False)
            new_im.save(buffer, im.format)
            buf_val = buffer.getvalue()
            image = ContentFile(buf_val)
            #TODO: корректную запись в БД
            image_file = InMemoryUploadedFile(image, None, out_name, 'image/jpeg', image.tell, None)
            print(image_file)
            self.image_resized = image_file
        elif self.image_link:
            name = str(self.image_link).split('/')[-1]
            img = NamedTemporaryFile(delete=True)
            img.write(urlopen(self.image_link).read())
            img.flush()
            self.image.save(name, File(img), save=False)
            self.image_resized.save(name, File(img), save=False)
            self.title = name
            # img.close()
        elif self.image:
            name = str(self.image).split('/')[-1]
            self.title = str(name)
            self.image_resized = self.image
        return super(ImageLoad, self).save()
