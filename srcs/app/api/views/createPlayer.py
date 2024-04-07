from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from django.contrib.auth.models import User
from app.models.Player import Player
from app.serializers import PlayerSerializer

from app import utils

class createPlayer(APIView):
	permission_classes = [utils.IsNotAuthenticated]

	def post(self, request, format=None):
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
