from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from app import utils

from django.contrib.auth.models import User
from app.models.Player import Player
from app.serializers import PlayerSerializer

class PlayerViewSet(ViewSet):
	permission_classes = [AllowAny]

	def create(self, request, player=None, format=None):
		errors = {}

		required_fields = ['username', 'email', 'password']
		for field in required_fields:
			field_data = request.data.get(field, None)
			if field_data is None:
				errors[field] = ['This field is required.']
			elif not field_data:
				errors[field] = ['This field may not be blank.']

			messages = utils.checkAvailability(field=field, field_data=field_data)
			print(f'messages: {messages}')
			if messages:
				errors[field] = messages

		if errors:
			return Response(errors, status=status.HTTP_400_BAD_REQUEST)
		
		try:
			new_user = User.objects.create_user(request.data['username'], '', request.data['password'])
			new_player = Player.objects.create(user=new_user, email=request.data['email'])
			serializer = PlayerSerializer(new_player, context={'scope' : 'private'})
			return Response(serializer.data)
		except Exception as e:
			return Response({'detail' : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

	def read(self, request, player, format=None):
		try:
			player_object = self.retrieve_player(player)
		except Exception as e:
			return Response({'detail' : str(e)}, status=status.HTTP_404_NOT_FOUND)
			
		if not player_object:
			return Response({'detail' : 'Ressource not found.'}, status=status.HTTP_404_NOT_FOUND)
		serializer = PlayerSerializer(player_object, context={'scope' : self.scope(), 'user' : request.user})
		return Response(serializer.data)
	
	def update(self, request, player, format=None):
		try:
			player_object = self.retrieve_player(player)
		except Exception as e:
			return Response({'detail' : str(e)}, status=status.HTTP_404_NOT_FOUND)

		serializer = PlayerSerializer(player_object, data=request.data, partial=True, context={'scope' : self.scope(), 'user' : request.user})
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
	def delete(self, request, player, format=None):
		try:
			player_object = self.retrieve_player(player)
		except Exception as e:
			return Response({'detail' : str(e)}, status=status.HTTP_404_NOT_FOUND)
		
		response = {}
		serializer = PlayerSerializer(player_object, context={'scope' : self.scope(), 'user' : request.user})
		field_name = 'confirm_destructive_action'
		required_field = request.data.get(field_name, None)
		if required_field is None:
			response[field_name] = ['This field is required.', 'Bool value expected']
			response['result'] = serializer.data
			return Response(response, status.HTTP_400_BAD_REQUEST)
		elif required_field is False:
			response[field_name] = ['Aborted.']
			response['result'] = serializer.data
			return Response(response, status.HTTP_406_NOT_ACCEPTABLE)
		else:
			user = player_object.user
			if user:
				user.delete()
			player_object.delete()
		return Response(serializer.data)

	def scope(self):
		return self.request.query_params.get('scope', None)
	
	def retrieve_player(self, player):
		try:
			player_object = Player.objects.get(pk=player)
		except ValidationError:
			try:
				user_object = User.objects.get(username=player)
				player_object = Player.objects.get(user=user_object.id)
			except Exception as e:
				raise e
		except Exception as e:
			raise e

		return player_object
