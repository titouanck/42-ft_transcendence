from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views.getRoutes import getRoutes
from .views.getPlayers import getPlayers
from .views.createPlayer import createPlayer
from .views.getPlayer import getPlayer
from .views.confirmEmail import confirmEmail

urlpatterns = [
    path('', getRoutes.as_view(), name='get_routes'),
    path('players/', getPlayers.as_view(), name='get_players'),
    path('players/new/', createPlayer.as_view(), name='create_player'),
    path('players/<str:player>/', getPlayer.as_view(), name='get_player'),
    path('confirm-email/', confirmEmail.as_view(), name='confirm_email'),
	path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
