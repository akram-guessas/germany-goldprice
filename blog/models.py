from django.db import models
# from django.contrib.auth.models import User
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.urls import reverse
from PIL import Image
from django.conf import settings

# Post tabel
class Post(models.Model):
    title = models.CharField(max_length=250, verbose_name='عنوان المقال')
    post_image = models.ImageField(null=True, blank=True, upload_to="images/", verbose_name='صورة المقال')
    content = RichTextField(null=True, blank=True, verbose_name='نص المقال')
    post_date = models.DateTimeField(default=timezone.now)
    post_update = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE , verbose_name='صاحب المقال')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            image = Image.open(self.post_image.path)
            image.save(self.post_image.path,quality=20,optimize=True)
        except:
            pass
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        #الأخبار/detail/عنوان%2001/13
        #.format(self.pk, self.title)
        return f'/detail/{self.title}/{self.pk}'
        #return reverse('detail', args=[self.title])
        #detail/<str:title>/<int:post_id>
    class Meta:
        ordering = ('-post_date',)

# Comment tabel
class Comment(models.Model):
    name = models.CharField(max_length=50, verbose_name='الاسم')
    email = models.EmailField(verbose_name='البريد الالكتروني')
    title = models.CharField(default='',max_length=200, verbose_name='عنوان التعليق')
    body = models.TextField(verbose_name='التعليق')
    comment_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    def __str__(self):
        return 'علق {} على {}.'.format(self.name, self.post)
    class Meta:
        ordering = ('-comment_date',)

class Contact(models.Model):
    name = models.CharField(max_length=50)
    email= models.EmailField(max_length=150)
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return self.name
