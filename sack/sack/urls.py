from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.authtoken.views import obtain_auth_token
from django.views.generic.base import RedirectView
from main.views import GetIcalView


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', GetIcalView.as_view(), name='get_ical'),
    url(r'^v1$', RedirectView.as_view(url='/v1/', permanent=False)),
    url(r'^v1/', include('main.urls')),
    url(r'^auth/', include('rest_framework.urls',
                           namespace='rest_framework')),
    url(r'^get-auth-token/', obtain_auth_token),
]
