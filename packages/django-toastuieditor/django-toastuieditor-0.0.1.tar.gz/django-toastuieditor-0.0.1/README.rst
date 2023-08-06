=====
Toastuieditor
=====

Toastuieditor 是一个django的应用程序，用于快速集成一个简单漂亮的markdown编辑器，支持html可视化渲染，基于开源程序toastui editor实现！

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "toastuieditor" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...,
        "toastuieditor",
    ]

2. Include the toastuieditor URLconf in your project urls.py like this::

    path("toastuieditor/", include("toastuieditor.urls")),

3. Run ``python manage.py migrate`` to create the polls models.

4. models中使用

    from toastuieditor.fields import ToastUIEditorHTMLField

    class ToastEditor(models.Model):
        content = ToastUIEditorHTMLField(verbose_name="内容")
    

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a poll (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/polls/ to participate in the poll.