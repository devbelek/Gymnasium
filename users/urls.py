from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UserProfileDetail, CommentViewSet, CommentReplyViewSet, LikeViewSet, DonationsViewSet, \
    ConfirmedDonationViewSet, RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.views import TokenObtainSlidingView, TokenRefreshSlidingView


router = DefaultRouter()
router.register(r'comments', CommentViewSet)
router.register(r'comment_replies', CommentReplyViewSet)
router.register(r'likes', LikeViewSet)
router.register(r'donations', DonationsViewSet)
router.register(r'confirmed_donations', ConfirmedDonationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('profile/', UserProfileDetail.as_view(), name='user-profile'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
]
