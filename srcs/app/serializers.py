from rest_framework import serializers
from django.contrib.auth.models import User
from app.models.Player import Player

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['username', 'email']

class PlayerSerializer(serializers.ModelSerializer):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if self.scope() == 'public':
			self.fields.pop('email', None)
   
	username = serializers.SerializerMethodField()
	email = serializers.SerializerMethodField()
		
	class Meta:
		model = Player
		fields = ['uid', 'username', 'email', 'player_rank', 'player_elo', 'total_victories', 'total_defeats', 'total_matches']
		
	def update(self, instance, validated_data):
		data = {}
		if 'username' in self.initial_data and instance.user:
			data['username'] = self.initial_data['username']
		if 'email' in self.initial_data and instance.user:
			data['email'] = self.initial_data['email']
			if data['email'] is None:
				data['email'] = ''
		user_serializer = UserSerializer(instance.user, partial=True, data=data)
		if user_serializer.is_valid():
			user_serializer.save()
		else:
			print(user_serializer.errors)
		return super().update(instance, validated_data)

	def get_username(self, obj):
		user = obj.user
		return user.username if user else None
		
	def get_email(self, obj):
		user = obj.user
		return user.email if user and user.email else None
		
	def scope(self):
		if not hasattr(self, 'context') or self.context.get('scope') != 'private':
			return 'public'
		else:
			return self.scope

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
	@classmethod
	def get_token(cls, user):
		token = super().get_token(user)
		token['username'] = user.username

		return token
