from django.urls import path

from . import views

urlpatterns = [
    path('', views.ImageListView.as_view(), name='index'),
    path('add/', views.AddImage.as_view(), name='add'),
    path('detail/<int:pk>', views.ImageView.as_view(), name='img-detail'),

]
