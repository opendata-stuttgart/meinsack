# coding=utf-8
from rest_framework.routers import Route, SimpleRouter

from .views import ZipCodeViewSet


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

urlpatterns = router.urls
