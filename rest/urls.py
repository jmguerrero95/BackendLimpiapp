from rest_framework import routers

from .viewsets import userViewSet
from .viewsets import auxiViewSet
from .viewsets import adminViewSet
from .viewsets import skillsViewSet
from .viewsets import tipo_modViewSet
from .viewsets import agend_ViewSet
from .viewsets import fecha_ViewSet2
from .viewsets import recuperar
#from .viewsets import recuperado

router = routers.SimpleRouter()
router.register('users', userViewSet)
router.register('auxi', auxiViewSet)
router.register('admin', adminViewSet)
router.register('skills', skillsViewSet)
router.register('tipo_mod', tipo_modViewSet)
router.register('agenda', agend_ViewSet)
router.register('fecha', fecha_ViewSet2)
router.register('recuperar', recuperar)
#router.register('recuperado', recuperado)
#router.('login', loginAPI.as_view())

urlpatterns = router.urls
