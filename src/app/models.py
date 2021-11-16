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

    # def save(self, *args, **kwargs):

    # if (self.width and self.height) or self.width or self.height:
    #     original_name, original_ext = os.path.splitext(self.image.name)
    #     out_name = f'{original_name}_resized{original_ext}'
    #     # TODO: Вынести в отдельный метод,
    #     im = Image.open(self.image.open())
    #     new_im = im.resize(size=self.sizing(self.width, self.height))
    #     buffer = BytesIO()
    #     self.image_resized.delete(save=False)
    #     new_im.save(buffer, im.format)
    #     buf_val = buffer.getvalue()
    #     image = ContentFile(buf_val)
    #     # TODO: корректную запись в БД
    #     image_file = InMemoryUploadedFile(image, None, out_name, 'image/jpeg', image.tell, None)
    #     print(image_file)
    #     self.image_resized = image_file
    # elif self.image_link:
    #     name = str(self.image_link).split('/')[-1]
    #     img = NamedTemporaryFile(delete=True)
    #     img.write(urlopen(self.image_link).read())
    #     img.flush()
    #     self.image.save(name, File(img), save=False)
    #     self.image_resized.save(name, File(img), save=False)
    #     self.title = name
    #     # img.close()
    # elif self.image:
    #     name = str(self.image).split('/')[-1]
    #     self.title = str(name)
    #     self.image_resized = self.image
    # # log.info("Test!!")
    # return super(ImageLoad, self).save()
