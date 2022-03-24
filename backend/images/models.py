from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class UploadedImage(models.Model):
    name = models.TextField(blank=True, default='')
    user = models.ForeignKey(User, related_name='images', on_delete=models.CASCADE)
    img = models.ImageField(upload_to='images/')
