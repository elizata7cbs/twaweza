from django.urls import path

from expenses.views import ExpenseCategoriesView

urlpatterns = [
    path('category/create/', ExpenseCategoriesView.as_view({'post': 'create'}), name='create'),
    path('category/list/', ExpenseCategoriesView.as_view({'get': 'list'}), name='list'),
]
