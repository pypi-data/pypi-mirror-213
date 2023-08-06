from django.template import Library
from django.template.loader import render_to_string
from django.conf import settings
from toastuieditor.widgets import TOAST_CONF

register = Library()

    
@register.simple_tag
def toast_view(value):
    
    css = (
        'https://uicdn.toast.com/editor/latest/toastui-editor.min.css'
        if TOAST_CONF.get('hasCDN', True) 
        else f'{settings.STATIC_URL}toastuieditor/toastui-editor.min.css'
    )
    js = (
        'https://uicdn.toast.com/editor/latest/toastui-editor-all.min.js'
        if TOAST_CONF.get('hasCDN', True) 
        else f'{settings.STATIC_URL}toastuieditor/toastui-editor-all.min.js'
    )    
    return render_to_string(
        "toastuieditor/viewer.html", 
        context={
            "value": value, 
            "toastuiedtior_css": css, 
            "toastuiedtior_js": js
        })
