from django.urls import path

from fee.views import FeeCategoriesView, FeeView

urlpatterns = [
    path('category/create/', FeeCategoriesView.as_view({'post': 'create'}), name='create'),
    path('category/list/', FeeCategoriesView.as_view({'get': 'list'}), name='list'),
    path('pay/', FeeView.as_view({'post': 'pay_fee'}), name='pay_fee'),
]
