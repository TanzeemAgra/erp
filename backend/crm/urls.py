"""
CRM App URLs - Customer Relationship Management
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'clients', views.ClientViewSet)
router.register(r'contacts', views.ContactPersonViewSet)
router.register(r'interactions', views.ClientInteractionViewSet)
router.register(r'opportunities', views.OpportunityViewSet)
router.register(r'tasks', views.TaskViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'choices', views.ChoicesViewSet, basename='choices')

urlpatterns = [
    path('', include(router.urls)),
]
