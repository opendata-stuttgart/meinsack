# coding=utf-8
from rest_framework import routers
from django.conf.urls import patterns, include, url

from .views import ZipCodeDetailView, ZipCodeListView

router = routers.DefaultRouter()

urlpatterns = patterns(
    '',
#    url(
#        regex=r'^', view=include(router.urls),
#    ),
    url(r'^$', ZipCodeListView.as_view()),
    url(r'^(?P<zipcode>\d{5})/$', ZipCodeDetailView.as_view()),
)
