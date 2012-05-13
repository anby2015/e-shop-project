from django.db import models
from django.contrib.auth.forms import User
from django.utils.translation import ugettext
from django.core.validators import RegexValidator

class Profile(models.Model):
    user = models.OneToOneField(User)
    info = models.TextField()
    validator=RegexValidator("\+\d{12}",ugettext("Wrong phone number"))
    tel = models.CharField(max_length=15,validators=[validator])
    city = models.CharField(max_length=60)
    photo = models.ImageField(upload_to='shop/static/profiles')
    def __unicode__(self):
        return self.user.username

class CompanyProfile(Profile):
    website = models.URLField()
    account = models.IntegerField()
    def __unicode__(self):
        return self.user.username


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
    category = models.ForeignKey(SubCategory,verbose_name=ugettext("Subcategory"))
    seller = models.ForeignKey(Profile)
    price = models.FloatField()
    description = models.TextField()
    photo = models.ImageField(upload_to='shop/static/products')
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
    author = models.ForeignKey(Profile,related_name='author')
    receiver = models.ForeignKey(Profile,related_name='receiver')
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
    picture = models.ImageField(upload_to='shop/static/banners')
    views = models.IntegerField()
    def __unicode__(self):
        return self.name


class News(models.Model):
    class Meta:
        verbose_name = ugettext("News")
        verbose_name_plural = ugettext("News")
    date = models.DateTimeField()
    title = models.CharField(max_length=300)
    text = models.TextField()
    picture = models.ImageField(upload_to='shop/static/news')
    def __unicode__(self):
        return self.title

class PurchaseAccount(models.Model):
    class Meta:
        verbose_name = ugettext("Purchase")
        verbose_name_plural = ugettext("Purchase")
    date = models.DateTimeField()
    user = models.ForeignKey(CompanyProfile)
    card = models.CharField(max_length=16)
    sum = models.IntegerField()
    def __unicode__(self):
        return self.user.user.username


class Deal(models.Model):
    """Is added to DB when shopping cart is confirmed"""
    DEAL_STATES = (
        (u'A', u'Added'),
        (u'S', u'Sold'),
        )
    action = models.CharField(max_length=1,choices=DEAL_STATES)
    date = models.DateTimeField()
    product = models.ForeignKey(Product)
    num = models.IntegerField()
    customer = models.ForeignKey(Profile,null=True,blank=True)