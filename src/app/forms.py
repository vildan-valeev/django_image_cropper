from django import forms
import requests
import urllib3
from django.core.validators import MaxValueValidator, MinValueValidator

from .models import *
from django.core.files.images import get_image_dimensions

log = logging.getLogger(__name__)


class ImageLoadForm(forms.ModelForm):
    image_link = forms.URLField(label='Ссылка', required=False, initial=None)

    class Meta:
        model = ImageLoad
        fields = ['image', 'image_link']

    @staticmethod
    def check_dict(clean_dict: dict) -> bool:
        """check dict. In dict will be only image or image_link (only one NoneType)"""
        # есть ли хоть один None, все ли значения в списке None
        if None in clean_dict.values() and all(isinstance(x, type(None)) for x in clean_dict.values()) is False:
            return True
        return False

    @staticmethod
    def is_url_image(image_link):
        """check  image_link url - will be image content"""
        image_formats = ("image/png", "image/jpeg", "image/jpg")
        r = requests.head(image_link)
        if r.headers["content-type"] in image_formats:
            return True
        return False

    @staticmethod
    def check_image(image):
        """check height and width image"""
        w, h = get_image_dimensions(image)
        print('w, h', w, h)
        if w > 2000:
            raise forms.ValidationError("The image is %i pixel wide. It's supposed to be 2000px" % w)
        if h > 2000:
            raise forms.ValidationError("The image is %i pixel high. It's supposed to be 2000px" % h)
        return True

    def clean(self, **kwargs):
        print('старт проверки')
        cleaned_data = super().clean()
        # log.info(msg=f'{cleaned_data=}')
        image = cleaned_data.get("image")
        image_link = cleaned_data.get("image_link")
        print(cleaned_data)
        if not self.check_dict(cleaned_data):
            raise forms.ValidationError('Либо фото, либо ссылку')

        if image:  # если изображение
            print('image', image)
            # прогрузка и проверка изображения
            self.check_image(image)

        if image_link:  # если только ссылка
            print('image_link', image_link)
            if not self.is_url_image(image_link):  # корректность ссылки
                raise forms.ValidationError('Ссылка не корректная. Это не изображение')
            # прогрузка и проверка изображения
            response = requests.get(image_link)
            b_img = BytesIO(response.content)

            print(b_img)
            self.check_image(b_img)
            i = InMemoryUploadedFile(b_img, image, b_img.name, 'image/jpeg', b_img.tell, None)
            cleaned_data["image"] = i
        print('finish cleaned_data', cleaned_data)
        return cleaned_data

    def clean_image_link(self):
        """Отлавливаем только пустой str"""
        image_link = self.cleaned_data.get("image_link")
        if len(image_link) == 0:
            image_link = None
        return image_link


class ImageResizeForm(forms.Form):
    width = forms.IntegerField(label='Ширина', required=False, max_value=2000, min_value=100)
    height = forms.IntegerField(label='Высота', required=False, max_value=2000, min_value=100)

    class Meta:
        fields = ['width', 'height']

    def clean(self):
        cleaned_data = super().clean()
        width = cleaned_data.get("width")
        height = cleaned_data.get("height")
        print(cleaned_data)
        # if self.width and self.height:
        #     if int(width) >= 2000 or int(height) >= 2000:
        #         raise ValidationError('Превышен максимальный размер!')
        #     size = self.sizing(self.image.width, self.image.height)
        #
        #     if round((self.width / size[0]), 1) != round((self.height / size[1]), 1):
        #         raise ValidationError(f'Укажите в пропорциях {self.image.width}x{self.image.height}. Или укажите только'
        #                               f' одно из значений')
        return cleaned_data
