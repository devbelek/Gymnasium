from django.urls import path, include
from .views import TeacherViews
from rest_framework import routers

routers = routers.SimpleRouter()
routers.register(r'profile', TeacherViews)

urlpatterns = [
    path('teacher/', include(routers.urls))
]