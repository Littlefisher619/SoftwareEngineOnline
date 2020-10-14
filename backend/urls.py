
from django.conf.urls import url
from django.urls import path, include

from .views.authviews import *
from .views.rateviews import RateViewSet
from .views.userviews import UserViewSetNormal
from .views.homwworkview import *
from .views.groupviews import *
from .views.judgementviews import *

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'signup', SignUpView, basename='注册')
router.register(r'login', LoginView, basename='登录')
router.register(r'user', UserViewSetNormal, basename='用户中心')
router.register(r'homework', HomeWorkViewSet, basename='作业')
router.register(r'group', GroupViewSet, basename='队伍')
router.register(r'judgement', JudgementViewSet, basename='评分')
router.register(r'rate', RateViewSet, basename='组长评分')

urlpatterns = [
    path(r'api/', include(router.urls))

]
