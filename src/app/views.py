from django.core.exceptions import ValidationError
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import FormMixin, ModelFormMixin

from app.forms import ImgForm, CropperForm
from app.models import Img


class ImgListView(ListView):
    """

    """
    model = Img
    context_object_name = 'image_list'
    queryset = Img.objects.all()
    template_name = 'app/img_list.html'


class ImgDetailView(ModelFormMixin, DetailView):
    """

    """
    model = Img
    form_class = CropperForm
    template_name = 'app/img_detail.html'
    # fields = ['width', 'height']


    def get_success_url(self):
        return reverse('img-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(ImgDetailView, self).get_context_data(**kwargs)
        context["form"] = self.get_form()
        return context

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
    model = Img
    form_class = ImgForm

    def get_success_url(self):
        return reverse('img-detail', kwargs={'pk': self.object.pk})
