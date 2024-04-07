from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.exceptions import ValidationError, ObjectDoesNotExist

import io
from rest_framework.parsers import JSONParser

from . import utils
from django.contrib.auth.models import User
from app.models.Player import Player
from app.serializers import PlayerSerializer

class getRoutes(APIView):
	authentication_classes = []
	permission_classes = [AllowAny]

	def get(self, request, format=None):
		routes = [
			'/api/players/',
			'/api/token/',
			'/api/token/refresh/'
		]
		return Response(routes)

class getPlayers(generics.ListAPIView):
	authentication_classes = []
	permission_classes = [AllowAny]
	serializer_class = PlayerSerializer

	def get_queryset(self):
		queryset = Player.objects.all()

		query_params = self.request.query_params.copy()
		
		if 'username' in query_params:
			query_params['user__username'] = query_params['username']
			query_params.pop('username')

		if 'email' in query_params:
			if self.scope() == 'private':
				query_params['user__email'] = query_params['email']
			query_params.pop('email')

		queryset = utils.filter(queryset, query_params)
		return queryset
	
	def get_serializer_context(self):
		context = super().get_serializer_context()
		context.update({"scope": self.scope()})
		return context

	def scope(self):
		return self.request.query_params.get('scope', None)

class getPlayer(APIView):
	authentication_classes = []
	permission_classes = [AllowAny]

	def get(self, request, player, format=None):
		player_object = self.retrieve_player(player)
		serializer = PlayerSerializer(player_object, context={'scope' : self.scope()})
		return Response(serializer.data)
	
	def patch(self, request, player, format=None):
		player_object = self.retrieve_player(player)
		serializer = PlayerSerializer(player_object, data=request.data, partial=True, context={'scope' : self.scope()})
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
	def get_serializer_context(self):
		context = super().get_serializer_context()
		context.update({"scope": self.scope()})
		return context

	def scope(self):
		return self.request.query_params.get('scope', None)
	
	def retrieve_player(self, player):
		try:
			player_object = Player.objects.get(pk=player)
		except ValidationError:
			try:
				user_object = User.objects.get(username=player)
				player_object = Player.objects.get(user=user_object.id)
			except (User.DoesNotExist, Player.DoesNotExist) as e:
				return Response({'detail' : str(e)}, status=status.HTTP_404_NOT_FOUND)
			except ValidationError as e:
				raise e
		return player_object

