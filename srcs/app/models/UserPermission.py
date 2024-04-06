from django.db import models
from uuid import uuid4
from .choices import CREATE, READ, UPDATE, DELETE

# **************************************************************************** #

class UserPermission(models.Model):

	uid = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)

	system_logs = models.SmallIntegerField(default=0)
	own_profile = models.SmallIntegerField(default=0)
	any_visible_profile = models.SmallIntegerField(default=READ)
	any_invisible_profile = models.SmallIntegerField(default=0)
	own_private_data = models.SmallIntegerField(default=0)
	any_private_data = models.SmallIntegerField(default=0)
	outgoing_message_to_friends = models.SmallIntegerField(default=0)
	outgoing_message_to_any = models.SmallIntegerField(default=0)
	incoming_message_from_friends = models.SmallIntegerField(default=0)
	incoming_message_from_any = models.SmallIntegerField(default=0)
	any_message = models.SmallIntegerField(default=0)
	own_relationships = models.SmallIntegerField(default=0)
	any_relationship = models.SmallIntegerField(default=0)
	own_permissions = models.SmallIntegerField(default=0)
	other_permissions = models.SmallIntegerField(default=0)

	ignore_recipient_message_restriction = models.BooleanField(default=False)

	# **************************************************************************** #

	def has_permission(self, permission, field_name):
		try:
			current_permissions = getattr(self, field_name)
			if current_permissions & permission == permission:
				return True
		except AttributeError as e:
			pass
		return False

	def add_permissions(self, permissions_to_add, field_name):
		try:
			current_permissions = getattr(self, field_name)
			for PERMISSION in [CREATE, READ, UPDATE, DELETE]:
				if permissions_to_add & PERMISSION == PERMISSION and current_permissions & PERMISSION != PERMISSION:
					current_permissions = current_permissions | PERMISSION
			setattr(self, field_name, current_permissions)
		except AttributeError as e:
			pass

	def remove_permissions(self, permissions_to_remove, field_name):
		try:
			current_permissions = getattr(self, field_name)
			for PERMISSION in [CREATE, READ, UPDATE, DELETE]:
				if permissions_to_remove & PERMISSION == PERMISSION and current_permissions & PERMISSION == PERMISSION:
					current_permissions = current_permissions & ~PERMISSION
			setattr(self, field_name, current_permissions)
		except AttributeError as e:
			pass

	def set_permissions(self, permissions_to_set, field_name):
		try:
			current_permissions = 0
			for PERMISSION in [CREATE, READ, UPDATE, DELETE]:
				if permissions_to_set & PERMISSION == PERMISSION and current_permissions & PERMISSION == PERMISSION:
					current_permissions = current_permissions | PERMISSION
			setattr(self, field_name, current_permissions)
		except AttributeError as e:
			pass

	# **************************************************************************** #

	def reset(self):
		fields = self._meta.fields
		for field in fields:
			if field.name not in ['uid']:
				setattr(self, field.name, field.get_default())

	def make_user(self):
		self.reset()
		self.add_permissions(READ | UPDATE | DELETE, 'own_profile')
		self.add_permissions(READ | UPDATE, 'own_private_data')
		self.add_permissions(CREATE | READ | DELETE, 'outgoing_message_to_friends')
		self.add_permissions(CREATE | READ | DELETE, 'outgoing_message_to_any')
		self.add_permissions(READ, 'incoming_message_from_friends')
		self.add_permissions(READ, 'incoming_message_from_any')
		self.add_permissions(CREATE | READ | UPDATE | DELETE, 'own_relationships')
		self.add_permissions(READ, 'own_permissions')

	def make_moderator(self):
		self.make_user()
		self.add_permissions(UPDATE, 'any_visible_profile')
		self.add_permissions(READ | UPDATE, 'any_invisible_profile')
		self.add_permissions(CREATE | READ | UPDATE | DELETE, 'any_relationship')
		self.add_permissions(READ, 'other_permissions')

		self.ignore_recipient_message_restriction = True
	
	# **************************************************************************** #

	def list_permissions(self, field_name):
		permissions_list = []
		try:
			current_permissions = getattr(self, field_name)
			for PERMISSION in [CREATE, READ, UPDATE, DELETE]:
				if current_permissions & PERMISSION == PERMISSION:
					permissions_list.append(PERMISSION)
		except AttributeError as e:
			pass
		return permissions_list
	