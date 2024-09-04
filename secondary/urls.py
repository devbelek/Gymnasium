from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import AdministratorTypesViewSet, NamesOfOlympiaViewSet, NameOfGradesViewSet, ContactsViewSet

router = DefaultRouter()
router.register(r'name_of_grades', NameOfGradesViewSet)
router.register(r'administrator_types', AdministratorTypesViewSet)
router.register(r'names_of_olympia', NamesOfOlympiaViewSet)
router.register(r'contacts', ContactsViewSet)

urlpatterns = [
    path('', include(router.urls)),

]