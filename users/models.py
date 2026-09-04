from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import os


class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    img = models.ImageField('Фото пользователя', default='default.png', upload_to='user_images')

    def __str__(self):
        return f'Профайл пользователя {self.user.username}'
    
    def save(self, *args, **kwargs):
        old = Profile.objects.filter(pk=self.pk).first()
        if old and old.img and old.img != self.img:
            if old.img.name != 'default.png' and os.path.isfile(old.img.path):
                os.remove(old.img.path)

        super().save(*args, **kwargs)

        image = Image.open(self.img.path)

        if image.height > 256 or image.width > 256:
            resize = (256, 256)
            image.thumbnail(resize)
            image.save(self.img.path)


    class Meta:
        verbose_name = 'Профайл'
        verbose_name_plural = 'Профайлы'
