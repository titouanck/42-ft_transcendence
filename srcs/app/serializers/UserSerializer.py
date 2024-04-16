from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .MyModelSerializer import MyModelSerializer
from django.contrib.auth.password_validation import validate_password as django_validate_password

# **************************************************************************** #

User._meta.get_field('username')._unique = True
User._meta.get_field('email')._unique = True

# **************************************************************************** #

class UserSerializer(MyModelSerializer):
	class Meta:
		model = User
		fields = ['username', 'email', 'password']
		read_only_fields = ['email']
		required_on_creation = ['username', 'password']

		extra_kwargs = {
			'username': {
				'required': False,
			},
			'password': {
				'required': False,
				'write_only': True
			}
		}

	# **************************************************************************** #

	def is_valid(self, raise_exception=False):
		super().is_valid(raise_exception=raise_exception)
		self.validate_fields()

		if self.errors and raise_exception:
			raise ValidationError(self.errors)
		return not self.errors
	
	def validate_password(self, data):
		password = self.initial_data.get('password', None)
		if password:
			try:
				django_validate_password(password)
			except ValidationError as e:
				raise e

	# **************************************************************************** #

	def update_password(self, instance, new_password):
		print('THIS IS CALLED')

		if 'password' in validated_data:
			instance.set_password(validated_data['password'])
			instance.save()
		return instance

	# def update(self, instance, validated_data):
	# 	instance = super().update(instance, validated_data)
	# 	if 'password' in validated_data:
	# 		instance.set_password(validated_data['password'])
	# 	instance = self.update_password(instance, validated_data)
	# 	return instance