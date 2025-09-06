"""
HR App URLs - Human Resources Management
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
# Will add ViewSets here as we create them

urlpatterns = [
    path('', include(router.urls)),
]
