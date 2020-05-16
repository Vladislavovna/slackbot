"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from polls.views import PollViewSet, QuestionViewSet, interactive_hook
from rest_framework_nested.routers import DefaultRouter, NestedSimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'polls', PollViewSet)

poll_router = NestedSimpleRouter(router, r'polls', lookup='poll')
poll_router.register(r'questions', QuestionViewSet, basename='poll-questions')

# urlpatterns = router.urls
urlpatterns = (
    # url(r'^', include(router.urls)),
    # url(r'^', include(poll_router.urls)),
    path('', admin.site.urls),
    # url('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # url('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('event/hook/', interactive_hook, name='event_hook'),
)
