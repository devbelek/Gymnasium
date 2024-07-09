from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import *


router = DefaultRouter()
router.register(r'students', StudentsViewSet)
router.register(r'thanks_note_from_students', ThanksNoteFromStudentsViewSet)
router.register(r'successful_graduates', SuccessfulGraduatesViewSet)
router.register(r'appeal_to_students', AppealToStudentsViewSet)
router.register(r'graduates', GraduatesViewSet)
router.register(r'thanks_note_from_graduates', ThanksNoteFromGraduatesViewSet)
router.register(r'news', NewsViewSet)
router.register(r'gallery', GalleryViewSet)
router.register(r'our_achievements', OurAchievementsViewSet)
router.register(r'teachers', TeachersViewSet)
router.register(r'feedback', FeedbackViewSet)
router.register(r'school_parliament', SchoolParliamentViewSet)
router.register(r'gimnasium_class', GimnasiumClassViewSet)
router.register(r'olympians', OlympiansViewSet)

urlpatterns = [
    path('', include(router.urls)),

]
