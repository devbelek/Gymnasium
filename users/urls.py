from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UserProfileDetail, CommentViewSet, CommentReplyViewSet, LikeViewSet, DonationsViewSet, ConfirmedDonationViewSet

router = DefaultRouter()
router.register(r'comments', CommentViewSet)
router.register(r'comment_replies', CommentReplyViewSet)
router.register(r'likes', LikeViewSet)
router.register(r'donations', DonationsViewSet)
router.register(r'confirmed_donations', ConfirmedDonationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('profile/', UserProfileDetail.as_view(), name='user-profile'),
]
