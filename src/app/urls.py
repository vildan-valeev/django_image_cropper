from django.urls import path

from . import views

urlpatterns = [
    path('', views.ImgListView.as_view(), name='index'),
    path('add/', views.AddImage.as_view(), name='add'),
    path('detail/<int:pk>', views.ImgDetailView.as_view(), name='img-detail'),
]
