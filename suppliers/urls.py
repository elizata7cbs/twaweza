from django.urls import path, include
from rest_framework.routers import DefaultRouter

from suppliers.views import SuppliersView


urlpatterns = [
    path('list/', SuppliersView.as_view({'get': 'list'}), name='list_suppliers'),
    path('create/', SuppliersView.as_view({'post': 'create'}), name='create_suppliers'),
]
