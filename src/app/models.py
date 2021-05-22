from urllib.request import urlopen

from PIL import Image
from django.core.exceptions import ValidationError
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.db import models
from django.urls import reverse


# TODO: add comments

class Img(models.Model):
    title = models.CharField(verbose_name='Название', max_length=300, blank=True, )
    img = models.ImageField(verbose_name='Файл', upload_to='images', )
    img_link = models.URLField(verbose_name='Ссылка', blank=True, null=True, )
    img_resized = models.ImageField(blank=True, null=True, upload_to='resized', )
    width = models.PositiveIntegerField(verbose_name='Ширина', blank=True, null=True, )
    height = models.PositiveIntegerField(verbose_name='Высота', blank=True, null=True, )

    def __str__(self):
        return self.title

    def clean(self):
        if self.width and self.height:
            if int(self.width) >= 2000 or int(self.height) >= 2000:
                raise ValidationError('Превышен максимальный размер!')
        # TODO: добавить валидацию на пропорции

    def get_absolute_url(self, *args, **kwargs):
        return reverse('image-view', kwargs={'pk': self.pk})

    def resize_img(self, *args, **kwargs):
        print(*args)
        print(*kwargs)
        # TODO: resize image and save
        # basewidth = 300
        # img = Image.open('fullsized_image.jpg')
        # wpercent = (basewidth / float(img.size[0]))
        # hsize = int((float(img.size[1]) * float(wpercent)))
        # img = img.resize((basewidth, hsize), Image.ANTIALIAS)
        # img.save('resized_image.jpg')
        resized = ...
        return resized




    def save(self, *args, **kwargs):
        print('args', args)
        print('kwargs', kwargs)
        print(self.width, self.height, self.img, self.img_link, self.pk)
        # TODO: переделать сохранение
        if (self.width and self.height) or self.width or self.height:
            print('изменение размера')
            self.resize_img(self.width, self.height, self.pk)
        if self.img_link:
            name = str(self.img_link).split('/')[-1]
            img = NamedTemporaryFile(delete=True)
            img.write(urlopen(self.img_link).read())
            img.flush()
            self.img.save(name, File(img))
            self.img_resized.save(name, File(img))
            # self.img_link = None
            self.title = name
        if self.img:

            name = str(self.img).split('/')[-1]
            self.img_resized = self.img
            self.title = str(name)
            # self.resize()
        # elif (self.width and self.height) or self.width or self.height:
        #     print('изменение размера')
        #     self.resize_img(self.width, self.height, self.pk)
        return super(Img, self).save()
        # super(Img, self).save()
