from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


# Create your views here.
def main(request):
    return render(request, "index.html")


def add_image(request):
    return render(request, "add.html")


def detail(request):
    return render(request, "detail.html")
