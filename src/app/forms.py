from django import forms
from .models import *


class ImageLoadForm(forms.ModelForm):

    class Meta:
        model = ImageLoad
        fields = ['image', 'image_link']

    def clean(self):
        cleaned_data = super().clean()
        if (cleaned_data['image'] is None and cleaned_data['image_link'] is None) or \
                (cleaned_data['image'] is not None and cleaned_data['image_link'] is not None):
            raise ValidationError('Либо фото, либо ссылку')
        return cleaned_data


class ImageResizeForm(forms.ModelForm):
    class Meta:
        model = ImageLoad
        fields = ['width', 'height']

    def clean(self):
        # print(f'{self.data=}')
        cleaned_data = super().clean()
        # print(f'{cleaned_data=}')
        if cleaned_data['width'] is None and cleaned_data['height'] is None:
            raise ValidationError('Введите хотя бы одно значение!')
        return cleaned_data
