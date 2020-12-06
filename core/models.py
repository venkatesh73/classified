from django.db import models
from django.conf import settings

class TimeStamps(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class Category(TimeStamps):
    name = models.CharField(max_length=255, null=False)
    code = models.CharField(max_length=16, null=False)
    active = models.BooleanField(default=True)
    logo = models.TextField(blank=False, null=False, default="img-1.png")

    def __str__(self):
        return self.name

class SubCategory(TimeStamps):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class City(TimeStamps):
    name = models.CharField(max_length=255, null=False)
    code = models.CharField(max_length=16, null=False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Classifieds(TimeStamps):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE) 
    cities = models.ManyToManyField(City)
    title = models.TextField(null=False)
    description = models.TextField(null=False)
    price = models.FloatField(blank=True, null=True)
    price_on_call = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    valid_till = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title

class ClassifiedsInterest(TimeStamps):
    classifieds = models.ForeignKey(Classifieds, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField(blank=False, null=False)

    def __str__(self):
        return  self.message

class ClassifiedsMedia(models.Model):
    classifieds = models.ForeignKey(Classifieds, on_delete=models.CASCADE)
    media_url = models.TextField(blank=False, null=False)
    type = models.CharField(max_length=50, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.media_url

class Profile(TimeStamps):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=25, null=False, blank=False, default="+91 0000-0000-00")

    def __str__(self):
        return self.user

