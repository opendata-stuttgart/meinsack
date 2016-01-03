from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.views.generic import TemplateView
from rest_framework.authtoken.views import obtain_auth_token

from main.views import GetIcalView


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', GetIcalView.as_view(), name='get_ical'),
    url(r'^faq/$', TemplateView.as_view(template_name='faq.html'), name='faq'),
    url(r'^legal/$', TemplateView.as_view(template_name='legal.html'), name='legal'),
    url(r'^v1$', RedirectView.as_view(url='/v1/', permanent=False)),
    url(r'^v1/', include('main.urls')),
    url(r'^auth/', include('rest_framework.urls',
                           namespace='rest_framework')),
    url(r'^get-auth-token/', obtain_auth_token),
]
