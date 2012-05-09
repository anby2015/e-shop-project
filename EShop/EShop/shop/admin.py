from models import *
from datetime import datetime
from django.contrib import admin

class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1

class CategoryAdmin(admin.ModelAdmin):
    list_per_page = 25
    ordering=['name']
    search_fields = ['name']
    inlines = [SubCategoryInline]
    
class SubCategoryAdmin(admin.ModelAdmin):
    list_per_page = 25
    ordering=['name']
    list_display = ['name','category']
    search_fields = ['name']
    list_filter = ['category']
    
class ProductAdmin(admin.ModelAdmin):
    list_per_page = 25
    fieldsets = [
                 [None,{
                 'fields' : ('name',('sub_category','seller'),'price','photo','description')}]
                ]
    list_display = ['name','seller','sub_category','price']
    ordering=['name']
    search_fields = ['name','seller__username']
    list_filter = ['sub_category__name']
    
class BannerAdmin(admin.ModelAdmin):
    list_per_page = 25
    list_display = ['name','url']
    ordering=['name']
    search_fields = ['name']
    
class NewsAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.date = datetime.now()
        obj.save()
    list_per_page = 25
    fields = ['title','picture','text']
    list_display = ['title','date']
    search_fields = ['title']
    list_filter = ['date']
    ordering = ['date']
    
class ProfileAdmin(admin.ModelAdmin):
    list_per_page = 25
    fieldsets = [
                 [None,{
                 'fields' : (('name','surname'),'user','photo',('city','tel'),'info')}]
                ]
    ordering = ['user']
    list_display = ['user','name','surname']
    search_fields = ['user__username','name','surname']
    
class CompanyProfileAdmin(admin.ModelAdmin):
    list_per_page = 25
    fieldsets = [
                 [None,{
                 'fields' : ('name','user','photo',('city','tel'),'website','state','info')}]
                ]
    ordering = ['user']
    list_display = ['user','name','state']
    search_fields = ['user__username','name']
    list_filter = ['state']
    
class WebFormularMessageAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
    list_per_page = 25
    fieldsets = [
                 [None,{
                 'fields' : (('email','date'),'state','message')}]
                ]
    readonly_fields = ['email','date','message']
    list_filter = ['date','state']
    ordering = ['date']
    search_fields = ['email']
    list_display = ['email','date','state']
    
class MessageAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
    list_per_page = 25
    fieldsets = [
                 [None,{
                 'fields' : (('author','receiver'),'date','message')}]
                ]
    readonly_fields = ['author','receiver','state','date','message']
    list_filter = ['date']
    ordering = ['date']
    search_fields = ['author__username','receiver__username']
    list_display = ['author','receiver','date']


admin.site.register(Profile,ProfileAdmin)
admin.site.register(CompanyProfile,CompanyProfileAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(SubCategory,SubCategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(WebFormularMessage,WebFormularMessageAdmin)
admin.site.register(Banner,BannerAdmin)
admin.site.register(News,NewsAdmin)
admin.site.register(Message,MessageAdmin)
