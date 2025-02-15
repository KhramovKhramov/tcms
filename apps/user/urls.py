from rest_framework import routers

from apps.user.api.views import AdministratorViewSet, UserViewSet

router = routers.SimpleRouter()

router.register(
    r'administrators', AdministratorViewSet, basename='administrators'
)
router.register('', UserViewSet, 'users')

urlpatterns = []
urlpatterns += router.urls
