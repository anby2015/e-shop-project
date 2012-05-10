from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'EShop.views.home', name='home'),
    # url(r'^EShop/', include('EShop.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/backup/$', 'shop.views.backup'),
    url(r'^admin/statistics/$', 'shop.views.statistics'),
    url(r'^admin/statistics_result', 'shop.views.statistics_result'),
    url(r'^admin/all_statistics', 'shop.views.all_statistics'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'shop.views.index'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)