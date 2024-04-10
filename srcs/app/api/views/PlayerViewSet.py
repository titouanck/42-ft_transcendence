from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from app import utils

from django.contrib.auth.models import User
from app.models.Player import Player
from app.serializers import PlayerSerializer

class PlayerViewSet(ViewSet):
	def create(self, request, player=None, format=None):
		serializer = PlayerSerializer(data=self.request.data)
		print(f'validity: {serializer.is_valid()}')
		print(f'errors: {serializer.errors}')
		return Response(serializer.errors)
		print(serializer.is_valid(is_staff=request.user.is_staff))
		print(serializer.errors)
		serializer.save()
		return Response(serializer.errors)
		# if request.user.is_authenticated and not request.user.is_staff:
		# 	return Response({"detail": "Impossible to create an account when already logged in."},  status=status.HTTP_403_FORBIDDEN)

		# errors = {}
		# required_fields = ['username', 'password']
		# if not request.user.is_staff:
		# 	required_fields.append('email_to_confirm')

		# for field in required_fields:
		# 	field_data = request.data.get(field, None)
		# 	if field_data is None:
		# 		errors[field] = ['This field is required.']
		# 	elif not field_data:
		# 		errors[field] = ['This field may not be blank.']

		# messages = utils.checkAvailability(field=field, field_data=field_data)
		# print(f'messages: {messages}')
		# if messages:
		# 	errors[field] = messages

		# if errors:
		# 	return Response(errors, status=status.HTTP_400_BAD_REQUEST)
		
		# new_user = new_player = None
		# try:
		# 	new_user = User.objects.create_user(request.data['username'], '', request.data['password'])
		# 	new_player = Player.objects.create(user=new_user, email=request.data['email'])
		# 	serializer = PlayerSerializer(new_player, context={'scope' : 'private'})
		# 	return Response(serializer.data)
		# except Exception as e:
		# 	try:
		# 		new_user.delete()
		# 		new_player.delete()
		# 	except Exception:
		# 		pass
		# 	return Response({'detail' : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
			if player_object.user != request.user and not request.user.is_staff:
				return Response({"detail": "Not enough permissions."},  status=status.HTTP_403_FORBIDDEN)
		except Exception as e:
			return Response({'detail' : str(e)}, status=status.HTTP_404_NOT_FOUND)

		serializer = PlayerSerializer(player_object, data=request.data, partial=True, context={'scope' : 'private', 'user' : request.user})
		if not serializer.is_valid(is_staff=request.user.is_staff):
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		serializer.save()
		player_object.clean()
		return Response(serializer.data)

	def delete(self, request, player, format=None):
		try:
			player_object = self.retrieve_player(player)
			if player_object.user != request.user and not request.user.is_staff:
				return Response({"detail": "Not enough permissions."},  status=status.HTTP_403_FORBIDDEN)
		except Exception as e:
			return Response({'detail' : str(e)}, status=status.HTTP_404_NOT_FOUND)

		response = {}
		serializer = PlayerSerializer(player_object, context={'scope' : 'private', 'user' : request.user})
		data = serializer.data
		field_name = 'confirm_destructive_action'
		required_field = request.data.get(field_name, None)
		if required_field is None:
			response[field_name] = ['This field is required.', 'Bool value expected']
			response['result'] = data
			return Response(response, status.HTTP_400_BAD_REQUEST)
		elif required_field is False:
			response[field_name] = ['Aborted.']
			response['result'] = data
			return Response(response, status.HTTP_400_BAD_REQUEST)
		else:
			user = player_object.user
			if user:
				user.delete()
			player_object.delete()
		return Response(data)

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
		
	def get_permissions(self):
		print(f'self.action: {self.action}')
		if self.action in ['read', 'update', 'delete']:
			permission_classes = [IsAuthenticatedOrReadOnly]
		else:
			permission_classes = [AllowAny]
		return [permission() for permission in permission_classes]

