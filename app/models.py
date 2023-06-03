from django.db import models
from django.conf import settings
from functools import partial
import time

def pathAndRename(instance, filename, upload):
    ext = filename.split('.')[-1]
    newName = time.time()
    filename = f"{newName}.{ext}"
    return f"{upload}{filename}"

class Shop(models.Model):
    title = models.TextField()
    description = models.TextField()
    image_url = models.FileField(upload_to=partial(pathAndRename, upload='shopAvatar/'), blank=True, null=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    in_category = models.ManyToManyField('self', blank=True, symmetrical=False)
    title = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.title


class Product(models.Model):
    in_shop = models.ForeignKey(Shop, on_delete=models.CASCADE, blank=True, null=True)
    in_category = models.ManyToManyField(Category, blank=True, symmetrical=False)
    title = models.TextField()
    description = models.TextField()
    amount = models.IntegerField()
    price = models.IntegerField()
    active = models.BooleanField()

    def __str__(self):
        return self.title


class ProductImages(models.Model):
    to_product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    image = models.FileField(upload_to=partial(pathAndRename, upload='productImages/'), blank=True, null=True)
    is_main = models.BooleanField(default=False)


class MakeWatermark(models.Model):
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    image_before = models.FileField(upload_to=partial(pathAndRename, upload='beforeWatermark/'), blank=True, null=True)
    image_after = models.FileField(upload_to=partial(pathAndRename, upload='afterWatermark/'), blank=True, null=True)
    done = models.BooleanField(default=False)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=40)
    surname = models.CharField(max_length=40)
    about = models.TextField(max_length=1000)
    avatar = models.FileField(upload_to=partial(pathAndRename, upload='profileAvatar/'), blank=True, null=True)
    balance = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    from_user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='from_user', blank=True, null=True)
    to_user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='to_user', blank=True, null=True)
    money = models.DecimalField(decimal_places=2, max_digits=1000, )
    date = models.DateTimeField(auto_now_add=True)
    done = models.BooleanField(default=False)
