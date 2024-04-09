from rest_framework import serializers
from django.contrib.auth.models import User
from app.models.Player import Player
from app.models.EmailVerification import EmailVerification
from django.db.models.query import QuerySet
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# **************************************************************************** #

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['username', 'email']

# **************************************************************************** #

class PlayerSerializer(serializers.ModelSerializer):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		many = True if isinstance(self.instance, QuerySet) else False
		if self.scope() == 'public' or (
			self.requester() and (
				(not self.requester() or not self.requester().is_staff
	 		) 
			and (
				many == True or self.requester() != self.instance.user)
			)
		):
			self.fields.pop('email', None)
			self.fields.pop('email_to_confirm', None)

	# **************************************************************************** #
 
	username = serializers.SerializerMethodField()
	email = serializers.SerializerMethodField()
	email_to_confirm = serializers.SerializerMethodField()
		
	class Meta:
		model = Player
		fields = ['uid', 'username', 'email', 'email_to_confirm', 'player_rank', 'player_elo', 'total_victories', 'total_defeats', 'total_matches']
		staff_only_fields = ['email', 'player_elo', 'total_victories', 'total_defeats']
		read_only_fields = ['uid', 'player_rank', 'total_matches']
		nullable_fields = ['email', 'email_to_confirm', 'player_elo']

	# **************************************************************************** #
 
	def is_valid(self, raise_exception=False, is_staff=False):
		super().is_valid(raise_exception=raise_exception)
		for key, value in self.initial_data.items():
			if key not in self.Meta.fields:
				self.add_error(key, 'This field do not exist.')
			elif key in self.Meta.read_only_fields:
				self.add_error(key, 'This field may not be updated.')
			elif key in self.Meta.staff_only_fields and not is_staff:
				self.add_error(key, 'This field can only be modified by a staff member.')
			elif value is None and key not in self.Meta.nullable_fields:
				self.add_error(key, 'This field may not be null.')
			
			elif key in ['username', 'email', 'email_to_confirm'] and value:
				original_key = key
				if key == 'email_to_confirm':
					key = 'email'
				filtered_users = User.objects.all().filter(**{key: value})
				for user in filtered_users:
					if user != self.instance.user:
						self.add_error(original_key, f'This {key} is already taken.')
				field = self.instance.user._meta.get_field(key)
				
				try:
					field.run_validators(value)
				except ValidationError as e:
					for error_message in e.messages:
						self.add_error(original_key, error_message)
				
				if key == 'email_to_confirm' and self.instance.user.email == value:
					self.add_error(original_key, "This email has already been confirmed.")

		if self.errors or self._errors:
			return False
		return True

	# **************************************************************************** #

	def update(self, instance, validated_data):
		data = {}
		for key, value in self.initial_data.items():
			if key in ['username', 'email']:
				if value:
					data[key] = value
				else:
					data[key] = ''
		
		user_serializer = UserSerializer(instance.user, partial=True, data=data)
		if user_serializer.is_valid():
			user_serializer.save()

		if 'email_to_confirm' in self.initial_data and instance.user:
			# TO DO
			pass
  
		return super().update(instance, validated_data)

	# **************************************************************************** #
 
	def get_username(self, obj):
		try:
			return obj.user.username if obj.user.username else None
		except Exception as e:
			return None
		
	def get_email(self, obj):
		try:
			return obj.user.email if obj.user.email else None
		except Exception as e:
			return None

	def get_email_to_confirm(self, obj):
		try:
			email_verification = EmailVerification.objects.get(user=obj.user)
			email_verification.update_all()
			return email_verification.email
		except Exception as e:
			return None
		
	# **************************************************************************** #
 
	def add_error(self, key, value):
		if key not in self._errors:
			self._errors[key] = []
		if value not in self._errors[key]:
			self.errors[key].append(value)

	def scope(self):
		if not hasattr(self, 'context') or self.context.get('scope') != 'private':
			return 'public'
		else:
			return self.context['scope']
		
	def requester(self):
		if not hasattr(self, 'context') or self.context.get('user', None) == None:
			return None
		else:
			return self.context['user']


# **************************************************************************** #

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
	@classmethod
	def get_token(cls, user):
		token = super().get_token(user)
		token['username'] = user.username

		return token
