from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User
# Create your models here.
class Book(models.Model):
    name = models.CharField( max_length=122)
    email = models.CharField(max_length=122)
    mobileno =  models.CharField(max_length=15)
    address = models.CharField( max_length=122)
    location = models.CharField( max_length=122)
    guests = models.IntegerField(validators=[MaxValueValidator(10)])
    arrivals = models.DateField()
    leaving  =  models.DateField()

    def __str__(self):
        return self.name
    
class Package(models.Model):
    ptitle = models.CharField( max_length=122,default="")
    pdays = models.CharField( max_length=122,default="")
    pdesc = RichTextField(default="")
    price = models.IntegerField(default=0)
    img = models.ImageField(upload_to='images',default="")
    acco = RichTextField(default="")
    meal = RichTextField(default="")
    inc = RichTextField(default="")
    
    def __str__(self):
        return self.ptitle


class Payment(models.Model):
    payment_id = models.CharField(max_length=100,null=True,blank=True)
    paid = models.BooleanField(default=False,null=True)

    
    