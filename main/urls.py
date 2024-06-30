from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import *


router = DefaultRouter()
router.register(r'nameofgrades', NameOfGradesViewSet)
router.register(r'administratortypes', AdministratorTypesViewSet)
router.register(r'students', StudentsViewSet)
router.register(r'thanksnotefromstudents', ThanksNoteFromStudentsViewSet)
router.register(r'namesofolympia', NamesOfOlympiaViewSet)
router.register(r'olympians', OlympiansViewSet)
router.register(r'successfulstudents', SuccessfulStudentsViewSet)
router.register(r'appealtostudents', AppealToStudentsViewSet)
router.register(r'graduates', GraduatesViewSet)
router.register(r'thanksnotefromgraduates', ThanksNoteFromGraduatesViewSet)
router.register(r'news', NewsViewSet)
router.register(r'gallery', GalleryViewSet)
router.register(r'ourachievements', OurAchievementsViewSet)
router.register(r'teachers', TeachersViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
