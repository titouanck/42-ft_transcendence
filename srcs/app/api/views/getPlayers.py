from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from django.contrib.auth.models import User
from app.models.Player import Player
from app.models.EmailVerification import EmailVerification
from app.serializers.PlayerSerializer import PlayerSerializer

from app import utils

def getPlayersQueryset(query_params, user, scope):
	queryset = Player.objects.all()

	if 'username' in query_params:
		query_params['user__username'] = query_params['username']
		query_params.pop('username')

	if 'email' in query_params:
		if scope == 'private' and user.is_staff:
			query_params['user__email'] = query_params['email']
		query_params.pop('email')

	return queryset

class getPlayers(generics.ListAPIView):
	permission_classes = [AllowAny]
	
	serializer_class = PlayerSerializer

	def get_queryset(self):
		return getPlayersQueryset(self.request.query_params.copy(), self.request.user, self.scope())
	
	def get_serializer_context(self):
		context = super().get_serializer_context()
		context.update({"scope": self.scope(), 'user' : self.request.user})
		return context

	def scope(self):
		return self.request.query_params.get('scope', None)
