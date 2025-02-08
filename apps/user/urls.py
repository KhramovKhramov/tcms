from rest_framework import routers

from apps.user.api.views import UserViewSet

router = routers.SimpleRouter()

router.register('', UserViewSet, 'users')

urlpatterns = []
urlpatterns += router.urls
