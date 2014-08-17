from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'shop.views.home', name='home'),
    url(r'^github_webhook/$', 'shop.views.github_webhook', name='github_webhook'),

    url(r'^admin/', include(admin.site.urls)),
)