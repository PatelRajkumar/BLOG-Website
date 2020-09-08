from django.conf.urls import include
from rest_framework import routers
from .views import PostCRUDCBV,CommentCRUDCBV
from django.urls import path
router=routers.DefaultRouter()
router.register('post',PostCRUDCBV)
router1=routers.DefaultRouter()
router1.register('comment',CommentCRUDCBV)
urlpatterns = [
    path('',include(router.urls)),
    path('',include(router1.urls )),
]
