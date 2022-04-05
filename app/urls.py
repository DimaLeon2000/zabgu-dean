from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path, include

router = DefaultRouter()  # create the router
router.register(r'specialties', SpecialtyViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'students', StudentViewSet)
router.register(r'sessions', SessionViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'marks', MarkViewSet)
router.register(r'marks_sorted', MarkViewSetSorted)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', indexView, name='index'),
    path('api/get_groups/<int:id_spec>', get_groups),
    path('api/get_students_spec/<int:id_spec>', get_students_spec),
    path('api/get_students_group/<int:id_group>', get_students_group),
    path('api/get_marks_spec/<int:id_spec>', get_marks_specialty),
    path('api/get_marks_specSort/<int:id_spec>', get_marks_specialty_sorted),
    path('api/get_marks_group/<int:id_group>', get_marks_group),
    path('api/get_marks_groupSort/<int:id_group>', get_marks_group_sorted),
    path('api/get_marks_student/<int:id_student>', get_marks_student),
    path('api/get_marks_studentSort/<int:id_student>', get_marks_student_sorted)
]
