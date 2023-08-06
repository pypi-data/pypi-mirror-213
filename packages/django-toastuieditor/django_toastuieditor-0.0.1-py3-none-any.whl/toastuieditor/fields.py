#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :fields.py
@说明    :ToastUIEditorField实现
@时间    :2023/05/30 12:00:04
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''


from typing import Any
from django.db.models.fields import TextField
from .widgets import ToastUIEditorTextareaHTML


class ToastUIEditorField(TextField):
    
    widget = None
    
    def formfield(self, **kwargs: Any) -> Any:
        if kwargs.get('widget'):
            kwargs['widget'] = self.widget or kwargs['widget']
        return super().formfield(**kwargs)


class ToastUIEditorHTMLField(ToastUIEditorField):
    
    widget = ToastUIEditorTextareaHTML
    