
from django.conf.urls import url
from django.urls import path, include

from .views.authviews import *
from .views.userviews import UserViewSetNormal

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'signup', SignUpView, basename='注册')
router.register(r'login', LoginView, basename='登录')
router.register(r'user', UserViewSetNormal, basename='用户中心')


urlpatterns = [
    path('', include(router.urls))

]
