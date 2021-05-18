# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import FormMixin

from app.forms import ImgForm, CropperForm
from app.models import Img


class ImgListView(ListView):
    """

    """
    model = Img
    context_object_name = 'image_list'
    queryset = Img.objects.all()
    template_name = 'app/img_list.html'


class ImgDetailView(FormMixin, DetailView):
    """

    """
    model = Img
    form_class = CropperForm

    def get_success_url(self):
        return reverse('author-detail', kwargs={'pk': self.object.pk})

    def post(self, request, *args, **kwargs):
        # image_inst = get_object_or_404(Img, pk=pk)
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # Here, we would record the user's interest using the message
        # passed in form.cleaned_data['message']
        return super().form_valid(form)


class AddImage(CreateView):
    """

    """
    template_name = 'app/img_create.html'
    model = Img
    form_class = ImgForm
    # success_url = reverse_lazy('img-detail')

    def get_success_url(self):
        return reverse('img-detail', kwargs={'pk': self.object.pk})

    # def get_form_kwargs(self, *args, **kwargs):
    #     kwargs = super(AddImage, self).get_form_kwargs(*args, **kwargs)
    #     return kwargs

