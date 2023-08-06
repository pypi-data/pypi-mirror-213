#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :widget.py
@说明    :widget部件
@时间    :2023/05/30 12:06:12
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''

from django.conf import settings
from django.forms.widgets import Textarea
from django.forms.renderers import get_default_renderer
from django.utils.safestring import mark_safe


LANGUAGE_MAPS = {
    'zh-hans': 'zh-CN',
    'zh-hant': 'zh-TW',
    'en-us': 'en-US',
}

DEFAULT_TOAST_CONF = {
    # 标记编辑器的预览样式（选项卡（tab），垂直(vertical)）
    "previewStyle":"vertical", 
    # 编辑器默认高度
    "height": "800px",
    # 编辑器最小高度样式
    "minHeight": "200px",
    # 是否高亮显示与标记编辑器中光标位置相对应的预览元素
    "previewHighlight": True,
    # 编辑器模式
    "initialEditType": "wysiwyg",
    # 是否允许切换模式
    "hideModeSwitch": False,
    # 是否发送到谷歌分析
    "usageStatistics": False,
    # 是否开启CDN外链
    "hasCDN": False,
    # 根据项目的语言变动
    "language": LANGUAGE_MAPS.get(settings.LANGUAGE_CODE.lower(), 'en-US')
}


TOAST_CONF = {**DEFAULT_TOAST_CONF, **settings.TOAST_CONF} if hasattr(settings, 'TOAST_CONF') else DEFAULT_TOAST_CONF


class ToastUIEditorWidget(Textarea):
    
    def __init__(self, attrs=None, toast_conf:dict=None) -> None:
        # 这里添加一组默认配置
        super().__init__(attrs)
        self.toast_conf = toast_conf or TOAST_CONF
    
    class Media:
        css = {'all': [
                ('https://uicdn.toast.com/editor/latest/toastui-editor.min.css'
                if TOAST_CONF.get('hasCDN', True) 
                else 'toastuieditor/toastui-editor.min.css'),
                'https://uicdn.toast.com/tui-color-picker/latest/tui-color-picker.min.css',
                'https://uicdn.toast.com/editor-plugin-color-syntax/latest/toastui-editor-plugin-color-syntax.min.css'
            ]
        }
        js = [
            ('https://uicdn.toast.com/editor/latest/toastui-editor-all.min.js'
            if TOAST_CONF.get('hasCDN', True) 
            else 'toastuieditor/toastui-editor-all.min.js'),
            f'toastuieditor/i18n/{TOAST_CONF.get("language").lower()}.min.js',
            'toastuieditor/plugins/uml/toastui-editor-plugin-uml.min.js',
            'https://uicdn.toast.com/tui-color-picker/latest/tui-color-picker.min.js',
            'https://uicdn.toast.com/editor-plugin-color-syntax/latest/toastui-editor-plugin-color-syntax.min.js',
        ]


class ToastUIEditorTextareaHTML(ToastUIEditorWidget):
    
    toast_template_name = "toastuieditor/toastuieditor.html"
    
    def render(self, name, value, attrs=None, renderer=None):
        context = {"name": name, "value": value, "toast": self.toast_conf}
        return super().render(name, value, attrs, renderer) + self.render_editor(context) 
    
    def render_editor(self, context):
        return mark_safe(get_default_renderer().render(self.toast_template_name, context))