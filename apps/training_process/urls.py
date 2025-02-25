from rest_framework import routers

from apps.training_process.api.views import (
    GroupApplicationViewSet,
    GroupViewSet,
)

router = routers.SimpleRouter()

router.register(
    r'group-applications',
    GroupApplicationViewSet,
    basename='group-applications',
)
router.register(r'groups', GroupViewSet, basename='groups')


urlpatterns = []
urlpatterns += router.urls
