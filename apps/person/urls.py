from rest_framework import routers

from apps.person.api.views import PersonViewSet

router = routers.SimpleRouter()

router.register('', PersonViewSet, 'persons')

urlpatterns = []
urlpatterns += router.urls