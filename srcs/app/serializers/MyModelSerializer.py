from rest_framework import serializers
from django.core.exceptions import ValidationError, FieldDoesNotExist

# **************************************************************************** #

class MyModelSerializer(serializers.ModelSerializer):
	class Meta:
		model = None
		fields = []
		read_only_fields = []
		required_on_creation = []

		extra_kwargs = {
		}

	# **************************************************************************** #

	def validate_fields(self):
		for key, value in self.initial_data.items():
			if key not in self.Meta.fields:
				self.add_error(key, 'This field do not exist.')
			elif key in self.Meta.read_only_fields:
				self.add_error(key, 'This field is read-only.')
			else:
				try:
					field = self.Meta.model._meta.get_field(key)	
					field.run_validators(value)
				except FieldDoesNotExist:
					pass
				except ValidationError as e:
					self.add_errors(key, e.messages)
		self.validate_on_creation()

	def validate_on_creation(self):
		if self.instance:
			return
		for field in self.Meta.required_on_creation:
			if field not in self.initial_data:
				self.add_error(field, 'This field is required.')

	# **************************************************************************** #
	
	def add_error(self, key, value):
		if key not in self._errors:
			self._errors[key] = []
		if value not in self._errors[key]:
			self.errors[key].append(value)

	def add_errors(self, key, values):
		for value in values:
			self.add_error(key, value)
