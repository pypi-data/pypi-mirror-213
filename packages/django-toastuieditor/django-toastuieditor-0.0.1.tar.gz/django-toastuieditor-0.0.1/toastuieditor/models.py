from django.db import models

# Create your models here.


class UploadImage(models.Model):
    
    img = models.ImageField("上传图", upload_to="editor/upload/%Y/", max_length=200)
    
    class Meta:
        verbose_name = "图片上传"
        verbose_name_plural = verbose_name
    
    def __str__(self) -> str:
        return self.img.name