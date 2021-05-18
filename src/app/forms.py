from django import forms
from .models import *


class ImgForm(forms.ModelForm):
    link = forms.URLField(label='Ссылка')

    class Meta:
        model = Img
        fields = '__all__'
    # TODO: validation - one of two field will be filled


class CropperForm(forms.Form):
    width = forms.IntegerField(label='Ширина')
    height = forms.IntegerField(label='Высота')
