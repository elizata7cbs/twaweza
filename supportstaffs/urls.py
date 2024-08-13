from django.urls import path

from supportstaffs.views import SupportCategoryView, SupportStaffView

urlpatterns = [
    path('category/create/', SupportCategoryView.as_view({'post': 'create'}), name='create'),
    path('category/list/', SupportCategoryView.as_view({'get': 'list'}), name='list'),
    path('staff/create/', SupportStaffView.as_view({'post': 'create'}), name='create'),
    path('staff/list/', SupportStaffView.as_view({'get': 'list'}), name='list'),

]
