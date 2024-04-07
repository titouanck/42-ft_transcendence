from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .views.getPlayers import getPlayers
from .views.PlayerViewSet import PlayerViewSet
from .views.confirmEmail import confirmEmail

class getRoutes(APIView):
	permission_classes = [AllowAny]

	def get(self, request, format=None):
		routes = []
		for pattern in urlpatterns:
			route = str(pattern).split('URLPattern ')[1].split('\'')[1]
			routes.append(f"api/{route}")
		return Response(routes)

urlpatterns = [
	path('', getRoutes.as_view(), name='get_routes'),
	path('players/', getPlayers.as_view(), name='get_players'),
	path('players/create/', PlayerViewSet.as_view({'post': 'create'}), name='create_player'),
	path('players/read/<str:player>/', PlayerViewSet.as_view({'get': 'read'}), name='read_player'),
	path('players/update/<str:player>/', PlayerViewSet.as_view({'patch': 'update'}), name='update_player'),
	path('players/delete/<str:player>/', PlayerViewSet.as_view({'delete': 'delete'}), name='delete_player'),
	path('confirm-email/<str:verification_slug>/', confirmEmail.as_view(), name='confirm_email'),
	path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
	path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
