from rest_framework import routers

from apps.training_process.api.views import GroupViewSet

router = routers.SimpleRouter()

router.register(r'groups', GroupViewSet, basename='groups')

urlpatterns = []
urlpatterns += router.urls
