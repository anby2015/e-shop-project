from models import *
from datetime import datetime
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    list_per_page = 25
    ordering = ['name']
    search_fields = ['name']
    inlines = [SubCategoryInline]


class SubCategoryAdmin(admin.ModelAdmin):
    list_per_page = 25
    ordering = ['name']
    list_display = ['name', 'category']
    search_fields = ['name']
    list_filter = ['category']


class ProductAdmin(admin.ModelAdmin):
    list_per_page = 2
    fieldsets = [
        [None, {
            'fields': ('name', ('category', 'seller'), 'price', 'photo', 'description')}]
    ]
    list_display = ['name', 'seller', 'category', 'price']
    ordering = ['name']
    search_fields = ['name', 'seller__username']
    list_filter = ['category__name']


class BannerAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not obj.views:
            obj.views = 0
        obj.save()
    readonly_fields = ['views']
    list_per_page = 25
    list_display = ['name', 'url','views']
    ordering = ['name']
    search_fields = ['name']


class NewsAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.date = datetime.now()
        obj.save()

    list_per_page = 25
    fields = ['title', 'picture', 'text']
    list_display = ['title', 'date']
    search_fields = ['title']
    list_filter = ['date']
    ordering = ['-date']


class ProfileAdmin(admin.ModelAdmin):
    list_per_page = 25
    fieldsets = [
        [None, {
            'fields': ('user', 'photo', ('city', 'tel'), 'info')}]
    ]
    ordering = ['user']
    list_display = ['user']
    search_fields = ['user__username']


class CompanyProfileAdmin(admin.ModelAdmin):
    list_per_page = 25
    fieldsets = [
        [None, {
            'fields': ('user', 'photo', ('city', 'tel'), 'website', 'state', 'info')}]
    ]
    ordering = ['user']
    list_display = ['user', 'state']
    search_fields = ['user__username', 'name']
    list_filter = ['state']


class WebFormularMessageAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    list_per_page = 25
    fieldsets = [
        [None, {
            'fields': (('email', 'date'), 'state', 'message')}]
    ]
    readonly_fields = ['email', 'date', 'message']
    list_filter = ['date', 'state']
    ordering = ['-date']
    search_fields = ['email']
    list_display = ['email', 'date', 'state']


class MessageAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    list_per_page = 25
    fieldsets = [
        [None, {
            'fields': (('author', 'receiver'), 'date', 'message')}]
    ]
    readonly_fields = ['author', 'receiver', 'state', 'date', 'message']
    list_filter = ['date']
    ordering = ['-date']
    search_fields = ['author__username', 'receiver__username']
    list_display = ['author', 'receiver', 'date']


class UserAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')}
            ),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        )

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(CompanyProfile, CompanyProfileAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(WebFormularMessage, WebFormularMessageAdmin)
admin.site.register(Banner, BannerAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Message, MessageAdmin)