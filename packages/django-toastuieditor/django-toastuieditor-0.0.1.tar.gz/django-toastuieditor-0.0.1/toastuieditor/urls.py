from django.urls import path
from . import views

app_name = "toastuieditor"

urlpatterns = [
    path('', views.ToastImageUploadView.as_view(), name='toast_img_upload'),
]