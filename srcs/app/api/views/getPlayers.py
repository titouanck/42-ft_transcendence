from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from django.contrib.auth.models import User
from app.models.Player import Player
from app.serializers import PlayerSerializer

from app import utils

class getPlayers(generics.ListAPIView):
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
