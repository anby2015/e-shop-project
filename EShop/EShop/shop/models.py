from django.db import models
from django.contrib.auth.forms import User

class Profile(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    user = models.ForeignKey(User)
    tel = models.CharField(max_length=15)
    city = models.CharField(max_length=60)
    additional = models.CharField(max_length=1000)
    photo = models.ImageField(upload_to='/tmp')
    
class CompanyProfile(models.Model):
    COMPANY_STATES = (
        (u'A', u'Active'),
        (u'B', u'Banned'),
    )
    
    name = models.CharField(max_length=30)
    info = models.CharField(max_length=1000)
    user = models.ForeignKey(User)
    tel = models.CharField(max_length=15)
    city = models.CharField(max_length=60)
    website = models.URLField()
    photo = models.ImageField(upload_to='/tmp')
    state = models.CharField(max_length=1, choices=COMPANY_STATES)
    
class Category(models.Model):
    #parent_category = models.ForeignKey(Category)
    name = models.CharField(max_length = 50)
    
class SubCategory(models.Model):
    name = models.CharField(max_length = 50)
    category = models.ForeignKey(Category)

class Product(models.Model):
    name = models.CharField(max_length=100)
    sub_category = models.ForeignKey(SubCategory)
    seller = models.ForeignKey(User)
    price = models.FloatField()
    description = models.CharField(max_length = 1000)
    photo = models.ImageField(upload_to='/tmp')
    
class WebFormularMessage(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    message = models.CharField(max_length = 2000)
    email = models.EmailField()
    
class Banner(models.Model):
    url = models.URLField()
    picture = models.ImageField(upload_to='/tmp')
    
class News(models.Model):
    date = models.DateTimeField()
    title = models.CharField(max_length = 300)
    text = models.CharField(max_length = 3000)
    picture = models.ImageField(upload_to='/tmp')
    
class Statictics(models.Model):
    since = models.DateField()
    total_sold = models.PositiveIntegerField()
    
class Deal(models.Model):
    "Is added to DB when shopping cart is confirmed"
    date = models.DateTimeField()
    products = models.ManyToManyField(Product)

    