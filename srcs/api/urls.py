from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import getRoutes, getPlayers, getPlayer, verify

urlpatterns = [
    path('', getRoutes.as_view(), name='get_routes'),
    path('verify/', verify.as_view(), name='verify'),
    path('players/', getPlayers.as_view(), name='get_players'),
    path('players/<str:player>/', getPlayer.as_view(), name='get_player'),
	path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
