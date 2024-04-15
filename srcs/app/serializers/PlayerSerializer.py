from rest_framework import serializers
from django.core.exceptions import ValidationError
from .MyModelSerializer import MyModelSerializer
from .UserSerializer import UserSerializer
from app.models.Player import Player

# **************************************************************************** #

class PlayerSerializer(MyModelSerializer):
	class Meta:
		model = Player
		fields = ['uid', 'username', 'email', 'password', 'player_rank', 'player_elo', 'total_victories', 'total_defeats', 'total_matches']
		read_only_fields = ['uid', 'player_rank', 'player_elo', 'total_victories', 'total_defeats', 'total_matches']
		required_on_creation = []

		user_fields = ['username', 'email', 'password']

		extra_kwargs = {
		}

	username = serializers.CharField(source='user.username', required=False)
	email = serializers.EmailField(source="user.email", required=False)
	password = serializers.CharField(write_only=True, required=False)

	# **************************************************************************** #

	def is_valid(self, raise_exception=False):
		super().is_valid(raise_exception=raise_exception)
		self.validate_fields()
		self.validate_user_fields()
		
		if self.errors and raise_exception:
			raise ValidationError(self.errors)
		return not self.errors
	
	def validate_user_fields(self):
		user = self.instance.user if self.instance else None
		user_initial_data = {}
		for field in self.Meta.user_fields:
			if field in self.initial_data:
				user_initial_data[field] = self.initial_data[field]
		user_serializer = UserSerializer(user, user_initial_data)
		if not user_serializer.is_valid():
			self._errors = self.errors | user_serializer.errors

# **************************************************************************** #
# **************************************************************************** #
# **************************************************************************** #
# **************************************************************************** #
# **************************************************************************** #
# **************************************************************************** #
# **************************************************************************** #
# **************************************************************************** #


# from rest_framework import serializers
# from django.contrib.auth.models import User
# from app.models.Player import Player
# from app.models.EmailVerification import EmailVerification
# from django.db.models.query import QuerySet
# from django.core.exceptions import ValidationError

# # **************************************************************************** #

# class PlayerSerializer(serializers.ModelSerializer):
# 	def __init__(self, *args, **kwargs):
# 		super().__init__(*args, **kwargs)
# 		many = True if isinstance(self.instance, QuerySet) else False

# 		# for field in self.fields:
# 		# 	if field in self.Meta.non_readable_fields:
# 		# 		self.fields.pop(field, None)

# 		# if self.scope() == 'public' or (
# 		# 	self.requester() and (
# 		# 		(not self.requester() or not self.requester().is_staff
# 	 	# 	) 
# 		# 	and (
# 		# 		many == True or self.requester() != self.instance.user)
# 		# 	)
# 		# ):
# 		# 	for field in self.fields:
# 		# 		if field in self.Meta.private_fields:
# 		# 			self.fields.pop(field, None)

# 	# **************************************************************************** #
 
# 	username = serializers.CharField(source='user.username', required=False)
# 	email = serializers.EmailField(source="user.email", required=False)
# 	email_to_confirm = serializers.SerializerMethodField()
# 	password = serializers.CharField(required=False, write_only=True)
	
# 	class Meta:
# 		model = Player
# 		fields = ['uid', 'username', 'email', 'email_to_confirm', 'player_rank', 'player_elo', 'total_victories', 'total_defeats', 'total_matches', 'password']

# 		editable_fields = ['username', 'email_to_confirm', 'password']
# 		required_for_creation = ['username', 'email_to_confirm', 'password']
# 		user_unique_fields = ['username', 'email_to_confirm']
# 		non_nullable_fields =['username', 'password']

# 	# **************************************************************************** #
 
# 	def to_representation(self, instance):
# 		data = super().to_representation(instance)
# 		for key, value in data.items():
# 			if value == '':
# 				data[key] = None
# 		return data

# 	# **************************************************************************** #
 
# 	def get_fields(self):
# 		fields = super().get_fields()
# 		if self.instance is None:
# 			for field in self.Meta.required_for_creation:
# 				fields[field].required = True
# 		return fields

# 	def get_email_to_confirm(self, obj):
# 		try:
# 			email_verification = EmailVerification.objects.get(user=obj.user)
# 			email_verification.update_all()
# 			return email_verification.email
# 		except Exception as e:
# 			return None

# 	# **************************************************************************** #

# 	def is_valid(self, raise_exception=False, is_staff=False):
# 		super().is_valid(raise_exception=raise_exception)
# 		for key, value in self.initial_data.items():
# 			if key not in self.Meta.fields:
# 				self.add_error(key, 'This field do not exist.')
			
# 			elif key not in self.Meta.editable_fields:
# 				self.add_error(key, 'This field may not be modified.')
			
# 			elif key in self.Meta.user_unique_fields and value:
# 				modified_key = key if key != 'email_to_confirm' else 'email'
# 				filtered_users = User.objects.all().filter(**{modified_key: value})
# 				for filtered_user in filtered_users:
# 					if not self.instance or self.instance.user != filtered_user:
# 						self.add_error(key, f'This {key} is already in use.')
				
# 				field = User._meta.get_field(modified_key)	
# 				try:
# 					field.run_validators(value)
# 				except ValidationError as e:
# 					for error_message in e.messages:
# 						self.add_error(key, error_message)

# 				if self.instance and modified_key == 'email_to_confirm' and self.instance.user.email == value:
# 					self.add_error(key, "This email has already been confirmed.")
# 			if key in self.Meta.non_nullable_fields or (not self.instance and key in self.Meta.required_for_creation):
# 				if value is None:
# 					self.add_error(key, 'This field may not be null.')
# 				elif not value:
# 					self.add_error(key, 'This field may not be blank.')

# 		if self.errors or self._errors:
# 			return False
# 		return True
	
# 	# **************************************************************************** #

# 	def update(self, instance, validated_data):
# 		data = {}
# 		print(f'hasattruser?: {hasattr(self.instance, "user")}')
# 		for key, value in self.initial_data.items():
# 			if key in ['username', 'email']:
# 				if value:
# 					data[key] = value
# 				else:
# 					data[key] = ''

# 		if 'email_to_confirm' in self.initial_data and instance.user:
# 			# TO DO
# 			pass

# 		response = super().update(instance, validated_data)
# 		self.instance.update_all()

# 		# user_serializer = UserSerializer(instance.user, partial=True, data=data)
# 		# if user_serializer.is_valid():
# 		# 	user_serializer.save()

# 		return response
		
# 	# **************************************************************************** #
 
# 	def add_error(self, key, value):
# 		if key not in self._errors:
# 			self._errors[key] = []
# 		if value not in self._errors[key]:
# 			self.errors[key].append(value)

# 	def scope(self):
# 		if not hasattr(self, 'context') or self.context.get('scope') != 'private':
# 			return 'public'
# 		else:
# 			return self.context['scope']
		
# 	def requester(self):
# 		if not hasattr(self, 'context') or self.context.get('user', None) == None:
# 			return None
# 		else:
# 			return self.context['user']

# # **************************************************************************** #
