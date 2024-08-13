from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static


from .views import StudentsView
router = DefaultRouter()
router.register(r'', StudentsView, basename='')


urlpatterns = [
    # path('', include(router.urls)),
    path('create/', StudentsView.as_view({'post': 'createStudent'}), name='createStudent'),
    path('list/', StudentsView.as_view({'get': 'list'}), name='listStudent'),
    path('search/', StudentsView.as_view({'get': 'search_student'}), name='search_student'),
    path('unpaginated/', StudentsView.as_view({'get': 'list_unpaginated'}), name='list_unpaginated'),
    path('students/create/', StudentsView.as_view({'post': 'createStudent'}), name='createStudent'),
    path('students/filter-students/<str:str>', StudentsView.as_view({'get': 'filter_students'}), name='filter_students'),
path('student/list_student_virtual_account', StudentsView.as_view({'get': 'list_student_virtual_account'}),
         name='list_student_virtual_account'),




 ]
