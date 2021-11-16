import os

from django.core.files.storage import default_storage
from django.db.models.fields.files import ImageFieldFile
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import ModelFormMixin, FormMixin, FormView
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from PIL import Image
from app.forms import ImageResizeForm, ImageLoadForm
from app.models import ImageLoad
from src.settings import MEDIA_ROOT


class AddImage(CreateView):
    """

    """
    template_name = 'app/img_create.html'
    model = ImageLoad
    form_class = ImageLoadForm

    def get_success_url(self):
        return reverse('img-detail', kwargs={'pk': self.object.pk})


class ImageListView(ListView):
    """

    """
    model = ImageLoad
    context_object_name = 'image_list'
    queryset = ImageLoad.objects.all()
    template_name = 'app/img_list.html'


class ImageDetailView(DetailView):
    """
    view after create and get detail
    """
    model = ImageLoad
    template_name = 'app/img_detail.html'

    def get_success_url(self):
        return reverse('img-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        """подсовываем форму в detail view"""
        context = super().get_context_data(**kwargs)
        context['form'] = ImageResizeForm()
        return context


class ImageResizeView(SingleObjectMixin, FormView):
    template_name = 'app/img_detail.html'
    form_class = ImageResizeForm
    model = ImageLoad

    def get_success_url(self):
        return reverse('img-detail', kwargs={'pk': self.object.pk})

    def post(self, request, *args, **kwargs):
        print('post')
        self.object = self.get_object()

        form = self.get_form()

        if form.is_valid():

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # def resize_image(self, image_field, width, height, name=None):
    #     """
    #     Resizes an image from a Model.ImageField and returns a new image as a ContentFile
    #     """
    #     img = Image.open(image_field)
    #     if img.size[0] > width or img.size[1] > height:
    #         new_img = img.resize((width, height))
    #     buffer = BytesIO()
    #     new_img.save(fp=buffer, format='JPEG')
    #     return ContentFile(buffer.getvalue())
    def sizing(self, image, width=None, height=None) -> tuple:
        """Рассчитываем пропорции"""
        size = None
        if width:
            width_percent = width / float(image.width)
            height_size = int((float(image.height) * float(width_percent)))
            size = (width, height_size)
        if height:
            height_percent = height / float(image.height)
            width_size = int((float(image.width) * float(height_percent)))
            size = (width_size, height)
        return size

    def form_valid(self, form):
        print('form_valid')
        # создаем новое изображение, сохраняем и подсовываем в object
        width = form.cleaned_data['width']
        height = form.cleaned_data['height']
        print('width', width)
        print('height', height)
        print('self.object', self.object, type(self.object))
        print(self.object.image.__dict__, type(self.object.image))

        pillow_image = Image.open(self.object.image)
        print(pillow_image)





        # new name
        # file_name, file_ext = os.path.splitext(self.object.title)  # ('my_image', '.jpg')
        # img_name = f'{file_name}_{width}_{height}{file_ext}'
        # # copy image
        # image_field = self.object.image
        # path = default_storage.save(f'{MEDIA_ROOT}/resized/{img_name}', ContentFile(image_field.read()))
        # tmp_file = os.path.join(MEDIA_ROOT, path)
        # print(tmp_file, path)
        # # resize image
        # pillow_image = Image.open(tmp_file)
        # pillow_image.
        # pillow_image = pillow_image.resize(self.sizing(pillow_image, width, height), Image.ANTIALIAS)
        # # TODO: переименовать изображение если пропорции не те которые введены
        # # pillow_image.save()
        #
        # print(pillow_image)

        # split_name = os.path.splitext(self.object.title)  # ('my_image', '.jpg')
        # img_name = f'{split_name[0]}_{width}_{height}{split_name[1]}'
        # img_path = MEDIA_ROOT / 'resized' / img_name
        #
        # pillow_image = self.resize_image(image_field, width=width, height=height, name=img_path)
        #
        # image_field.save(
        #     img_name,
        #     InMemoryUploadedFile(
        #         pillow_image,  # file
        #         None,  # field_name
        #         img_name,  # file name
        #         'image/jpeg',  # content_type
        #         pillow_image.tell,  # size
        #         None)  # content_type_extra
        # )
        #
        #
        # print(image_field)

        # self.object.image = image_field

        return super().form_valid(form)


class ImageView(View):

    def get(self, request, *args, **kwargs):
        view = ImageDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ImageResizeView.as_view()
        return view(request, *args, **kwargs)
