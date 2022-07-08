from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.db.models.signals import post_save
from PIL import Image
from django.conf import settings

class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
    	return self.user.username

class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone=models.CharField(max_length=200)
    address=models.CharField(max_length=200)
    is_active = models.BooleanField(default=False)

    def __str__(self):
    	return self.user.username

class Item(models.Model):
    item_name = models.CharField(max_length=250, verbose_name='عنوان المنتج')
    item_image = models.ImageField(blank=True, upload_to="item_pics/", verbose_name='صورة المنتج')
    price = models.FloatField(verbose_name='سعر المنتج')
    phone_numb = models.CharField(null=True, blank=True, max_length=20, verbose_name='رقم الهاتف')
    address = models.CharField(null=True, blank=True, max_length=100, verbose_name='العنوان')
    # discount_price = models.FloatField(blank=True, null=True)
    # category = models.CharField(choices=CATEGORY, max_length=2)
    # label = models.CharField(max_length=2)
    # description = models.TextField()
    description = RichTextField(null=True, blank=True, verbose_name='الوصف')
    item_date = models.DateTimeField(verbose_name='تاريخ العرض', default=timezone.now)
    item_update = models.DateTimeField(verbose_name='تاريخ التحديث', auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE , verbose_name='البائع')

    def __str__(self):
        return self.item_name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            image = Image.open(self.item_image.path)
            image.save(self.item_image.path,quality=20,optimize=True)
        except:
            pass
    
    def get_absolute_url(self):
        #الأخبار/detail/عنوان%2001/13
        #.format(self.pk, self.title)
        return 'detail/' + f'{self.item_name}/{self.pk}'
        #return reverse('detail', args=[self.title])
        #detail/<str:title>/<int:post_id>
    class Meta:
        ordering = ('-item_date',)
        

class Profile(models.Model):
    image = models.ImageField(default='images/default.png', upload_to='profile_pics')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return '{} profile.'.format(self.user.username)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.width > 300 or img.height > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


def create_profile(sender, **kwarg):
    if kwarg['created']:
        Profile.objects.create(user=kwarg['instance'])


post_save.connect(create_profile, sender=User)
