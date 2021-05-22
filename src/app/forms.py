from django import forms
from .models import *


class ImgForm(forms.ModelForm):
    # link = forms.URLField(label='Ссылка')

    class Meta:
        model = Img
        fields = ['img', 'img_link']

    def clean(self):

        cleaned_data = super().clean()
        if (cleaned_data['img'] is None and cleaned_data['img_link'] is None) or \
                (cleaned_data['img'] is not None and cleaned_data['img_link'] is not None):
            raise ValidationError('Либо фото, либо ссылку')
        return cleaned_data


class CropperForm(forms.ModelForm):
    class Meta:
        model = Img
        fields = ['width', 'height']

    def clean(self):
        print(f'{self.data=}')
        cleaned_data = super().clean()
        print(f'{cleaned_data=}')
        if cleaned_data['width'] is None and cleaned_data['height'] is None:
            raise ValidationError('Введите хотя бы одно значение!')
        return cleaned_data
