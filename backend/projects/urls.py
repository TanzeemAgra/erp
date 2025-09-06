"""
Projects App URLs - Project Management
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'projects', views.ProjectViewSet)
router.register(r'tasks', views.TaskViewSet)
router.register(r'time-entries', views.TimeEntryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
