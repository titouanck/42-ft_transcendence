from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User
from app.models.Player import Player
from app.serializers import PlayerSerializer

class getPlayer(APIView):
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
