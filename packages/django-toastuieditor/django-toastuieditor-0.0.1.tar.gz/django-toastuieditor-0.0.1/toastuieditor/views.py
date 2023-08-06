from typing import Any
from django import forms
from django.shortcuts import render
from django.http.response import JsonResponse
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

from .models import UploadImage


class ToastImageForm(forms.ModelForm):
    
    class Meta:
        model = UploadImage
        fields = ("img", )


class ToastImageUploadView(LoginRequiredMixin, View):
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args: Any, **kwargs: Any):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        form = ToastImageForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
        return JsonResponse({'code': 'ok', 'url': obj.img.url, 'text': obj.img.name})
