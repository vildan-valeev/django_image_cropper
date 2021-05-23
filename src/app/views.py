from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import ModelFormMixin

from app.forms import ImageResizeForm, ImageLoadForm
from app.models import ImageLoad


class ImageListView(ListView):
    """

    """
    model = ImageLoad
    context_object_name = 'image_list'
    queryset = ImageLoad.objects.all()
    template_name = 'app/img_list.html'


class ImageDetailView(ModelFormMixin, DetailView):
    """

    """
    model = ImageLoad
    form_class = ImageResizeForm
    template_name = 'app/img_detail.html'

    # fields = ['width', 'height']

    def get_success_url(self):
        return reverse('img-detail', kwargs={'pk': self.object.pk})

    # def get_context_data(self, **kwargs):
    #     context = super(ImageDetailView, self).get_context_data(**kwargs)
    #     context["form"] = self.get_form()
    #     return context
    #
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        return super().form_valid(form)


class AddImage(CreateView):
    """

    """
    template_name = 'app/img_create.html'
    model = ImageLoad
    form_class = ImageLoadForm

    def get_success_url(self):
        return reverse('img-detail', kwargs={'pk': self.object.pk})

    # def get_context_data(self, **kwargs):
    #     context = super(AddImage, self).get_context_data(**kwargs)
    #     context['form'] = ImageLoadForm
    #     return context
    #
    # def post(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     form = self.get_form()
    #     if form.is_valid():
    #
    #         return self.form_valid(form)
    #     else:
    #         return self.form_invalid(form)
    #
    # def form_valid(self, form):
    #     return super().form_valid(form)