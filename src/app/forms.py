from django import forms
from .models import *

log = logging.getLogger(__name__)


class ImageLoadForm(forms.ModelForm):
    class Meta:
        model = ImageLoad
        fields = ['image', 'image_link']

    def check_dict(self, clean_dict: dict) -> bool:
        """check dict. In dict will be only image or image_link (only one NoneType)"""
        # есть ли хоть один None, все ли значения в списке None
        if None in clean_dict.values() and all(isinstance(x, type(None)) for x in clean_dict.values()) is False:
            return True
        return False

    def clean(self, **kwargs):
        print(kwargs)
        cleaned_data = super().clean()
        log.info(msg=f'{cleaned_data=} {type(cleaned_data)}')

        if not self.check_dict(cleaned_data):
            return forms.ValidationError('Либо фото, либо ссылку')

        # if not None in cleaned_data.values():

        # if (cleaned_data['image'] is None and cleaned_data['image_link'] is None) or \
        #         (cleaned_data['image'] is not None and cleaned_data['image_link'] is not None):
        #     raise forms.ValidationError('Либо фото, либо ссылку')
        # if self.width and self.height:
        #     if int(self.width) >= 2000 or int(self.height) >= 2000:
        #         raise ValidationError('Превышен максимальный размер!')
        #     size = self.sizing(self.image.width, self.image.height)
        #
        #     if round((self.width / size[0]), 1) != round((self.height / size[1]), 1):
        #         raise ValidationError(f'Укажите в пропорциях {self.image.width}x{self.image.height}. Или укажите только'
        #                               f' одно из значений')
        return cleaned_data


class ImageResizeForm(forms.ModelForm):
    class Meta:
        model = ImageLoad
        fields = ['image', 'image_link']
        # fields = ['width', 'height']

    # def clean(self):
    #     # print(f'{self.data=}')
    #     cleaned_data = super().clean()
    #     # print(f'{cleaned_data=}')
    #     if cleaned_data['width'] is None and cleaned_data['height'] is None:
    #         raise ValidationError('Введите хотя бы одно значение!')
    #     return cleaned_data
