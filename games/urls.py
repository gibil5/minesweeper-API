"""games URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers, serializers, viewsets
from rest_framework.schemas import get_schema_view
from minesweeper import views, api_views

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'boards', api_views.BoardViewSet)
#router.register(r'cells', api_views.CellViewSet)
router.register(r'users', api_views.UserViewSet)
#router.register(r'groups', views.GroupViewSet)

# Routing
urlpatterns = [
    # Users
    path('', include("users.urls")),

    path('admin/', admin.site.urls),

    # Game
    path('boards/', include("minesweeper.urls")),

    # Rest
    path('rest/', include(router.urls)),
    path('rest/board_init/', api_views.BoardInit.as_view()),
    path('rest/board_update/', api_views.BoardUpdate.as_view()),
    path('rest/board_check/', api_views.BoardCheck.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Api documentation
    # With swagger
    path('swagger-ui/', TemplateView.as_view(
        template_name='minesweeper/swagger-ui.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='swagger-ui'),
    # With openapi
    path('openapi', get_schema_view(
        title="minesweeper-API",
        description="REST API for the Minesweeper game.",
        version="1.0.0"
    ), name='openapi-schema'),
    # With redoc
    path('redoc/', TemplateView.as_view(
        template_name='minesweeper/redoc.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='redoc'),
]
