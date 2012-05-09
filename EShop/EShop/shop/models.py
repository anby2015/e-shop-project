from django.db import models
from django.contrib.auth.forms import User
from django.utils.translation import ugettext
from django.core.validators import RegexValidator

class UserInfo(models.Model):
    name = models.CharField(max_length=30)
    info = models.TextField()
    user = models.ForeignKey(User)
    validator=RegexValidator("\+\d{12}",ugettext("Wrong phone number"))
    tel = models.CharField(max_length=15,validators=[validator])
    city = models.CharField(max_length=60)
    photo = models.ImageField(upload_to='tmp')


class Profile(UserInfo):
    surname = models.CharField(max_length=30)
    def __unicode__(self):
        return self.surname


class CompanyProfile(UserInfo):
    COMPANY_STATES = (
        (u'A', u'Active'),
        (u'B', u'Banned'),
        )
    website = models.URLField()
    state = models.CharField(max_length=1, choices=COMPANY_STATES)
    def __unicode__(self):
        return self.name


class Category(models.Model):
    class Meta:
        verbose_name = ugettext("Category")
        verbose_name_plural = ugettext("Categories")
    name = models.CharField(max_length=50)
    def __unicode__(self):
        return self.name


class SubCategory(models.Model):
    class Meta:
        verbose_name = ugettext("Subcategory")
        verbose_name_plural = ugettext("Subcategories")
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category)
    def __unicode__(self):
        return self.name


class Product(models.Model):
    class Meta:
        verbose_name = ugettext("Product")
        verbose_name_plural = ugettext("Products")
    name = models.CharField(max_length=100)
    sub_category = models.ForeignKey(SubCategory,verbose_name=ugettext("Subcategory"))
    seller = models.ForeignKey(User)
    price = models.FloatField()
    description = models.TextField()
    photo = models.ImageField(upload_to='tmp')
    def __unicode__(self):
        return self.name

class Message(models.Model):
    class Meta:
        verbose_name = ugettext("Message")
        verbose_name_plural = ugettext("Messages")
    MESSAGE_STATES = (
        (u'O', u'Old'),
        (u'N', u'New'),
        )
    state = models.CharField(max_length=1, choices=MESSAGE_STATES)
    date = models.DateTimeField()
    author = models.ForeignKey(User,related_name='author')
    receiver = models.ForeignKey(User,related_name='receiver')
    message = models.TextField()

class WebFormularMessage(models.Model):
    class Meta:
        verbose_name = ugettext("WebMessage")
        verbose_name_plural = ugettext("WebMessages")
    MESSAGE_STATES = (
        (u'O', u'Old'),
        (u'N', u'New'),
        )
    state = models.CharField(max_length=1, choices=MESSAGE_STATES)
    date = models.DateTimeField()
    message = models.TextField()
    email = models.EmailField()


class Banner(models.Model):
    class Meta:
        verbose_name = ugettext("Banner")
        verbose_name_plural = ugettext("Banners")
    name = models.CharField(max_length=100)
    url = models.URLField()
    picture = models.ImageField(upload_to='tmp')
    def __unicode__(self):
        return self.name


class News(models.Model):
    class Meta:
        verbose_name = ugettext("News")
        verbose_name_plural = ugettext("News_p")
    date = models.DateTimeField()
    title = models.CharField(max_length=300)
    text = models.TextField()
    picture = models.ImageField(upload_to='tmp')
    def __unicode__(self):
        return self.title


class Deal(models.Model):
    """Is added to DB when shopping cart is confirmed"""
    date = models.DateTimeField()
    products = models.ManyToManyField(Product)
    sum = models.IntegerField()