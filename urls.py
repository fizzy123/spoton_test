from django.conf.urls import patterns, url

from spoton_test import views

urlpatterns = patterns('spoton_test.views',
        url(r'^$', 'get_addresses', name='get_addresses'),
        )
