# coding=utf-8
from django.conf.urls import include, url
from rest_framework.routers import Route, SimpleRouter, DynamicDetailRoute

from .views import ZipCodeViewSet, StreetViewSet


class ZipCodeRouter(SimpleRouter):
    routes = [
        Route(
            url=r'^$',
            mapping={'get': 'list'},
            name='{basename}-list',
            initkwargs={'suffix': 'List'}
        ),
        Route(
            url=r'^{lookup}/$',
            mapping={'get': 'retrieve'},
            name='{basename}-detail',
            initkwargs={'suffix': 'Detail'}
        ),
    ]

router = ZipCodeRouter()
router.register('zipcode', ZipCodeViewSet, base_name="zipcode")


class StreetRouter(SimpleRouter):
    routes = [
        Route(
            url=r'^(?P<zipcode>\w+)/{lookup}/$',
            mapping={'get': 'retrieve'},
            name='{basename}-detail',
            initkwargs={'suffix': 'Detail'}
        ),
        DynamicDetailRoute(
            url=r'^(?P<zipcode>\w+)/{lookup}/{methodnamehyphen}/$',
            name='{basename}-{methodnamehyphen}',
            initkwargs={}
        )
    ]

street_router = StreetRouter()
street_router.register('street', StreetViewSet, base_name="street")

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(street_router.urls)),
]
