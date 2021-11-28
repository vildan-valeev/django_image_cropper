import os
from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView

from app.forms import ImageResizeForm, ImageLoadForm
from app.models import ImageLoad
from app.services import Resizer
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
    """
        view when resize and POST
    """
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

    # def form_valid(self, form, **kwargs):
    #     print('form_valid')
    #     # создаем новое изображение, сохраняем и подсовываем в object
    #     width = form.cleaned_data['width']
    #     height = form.cleaned_data['height']
    #     print('width', width)
    #     print('height', height)
    #
    #     original_name, original_ext = os.path.splitext(self.object.title)
    #     out_name = f'{original_name}_{width}_{height}{original_ext}'
    #     img = Image.open(self.object.image.open())
    #     new_im = img.resize(size=(width, height))
    #     buffer = BytesIO()
    #     new_im.save(buffer, img.format)
    #     image = ContentFile(buffer.getvalue())
    #     image_file = InMemoryUploadedFile(image, None, out_name, 'image/jpeg', image.tell, None)
    #     tmp = os.path.join(MEDIA_ROOT, "resized", out_name)
    #     default_storage.save(tmp, image_file)
    #     context = self.get_context_data(**kwargs)
    #     context['imageload'] = ImageLoad(title=out_name, image=os.path.join("resized", out_name))
    #     return self.render_to_response(context)

    def form_valid(self, form, **kwargs):
        print('form_valid')
        # создаем новое изображение, сохраняем и подсовываем в object
        width = form.cleaned_data['width']
        height = form.cleaned_data['height']
        print('width', width)
        print('height', height)
        resizer = Resizer(self.object)
        resizer.resize(width=width, height=height)
        context = self.get_context_data(**kwargs)
        context['imageload'] = ImageLoad(title=resizer.get_out_name(), image=os.path.join("resized", resizer.get_out_name()))
        return self.render_to_response(context)

class ImageView(View):
    """view for get/post image"""

    def get(self, request, *args, **kwargs):
        view = ImageDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ImageResizeView.as_view()
        return view(request, *args, **kwargs)
