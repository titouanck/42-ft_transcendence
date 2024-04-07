from django.db.models import Q
from django.contrib.auth.models import User
from django.core.exceptions import FieldError, ValidationError, ObjectDoesNotExist
from rest_framework.permissions import BasePermission
import re

class IsNotAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return not request.user or not request.user.is_authenticated

def filter(queryset, query_params):
	for field_name, field_value in query_params.items():
		if field_value:
			q_objects = Q()
			args = field_value.split(',')
			for arg in args:
				arg = arg.strip()
				if arg:
					key = field_name
					if arg[0] == '^':
						key += '__istartswith'
						arg = arg[1:]
					elif arg[0] == '!':
						key += '__icontains'
						arg = arg[1:]
					
					if arg == 'null':
						filter_kwargs = {field_name + '__isnull' : True}
						q_objects |= Q(**filter_kwargs)
						filter_kwargs = {field_name : ''}
						q_objects |= Q(**filter_kwargs)
					elif arg:
						filter_kwargs = {key : arg}
						q_objects |= Q(**filter_kwargs)
			try:
				queryset = queryset.filter(q_objects)
			except FieldError:
				pass
			except (ValueError, ValidationError, Exception):
				return []
	return queryset

def isEmailValid(email):
	regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
	if re.match(regex, email):
		return True
	return False

def checkAvailability(field=None, field_data=None):
	if field and field_data:
		try:
			if field == 'username':
				User.objects.get(username=field_data)
			elif field == 'email':
				if isEmailValid(field_data):
					User.objects.get(email=field_data)
			else:
				raise ObjectDoesNotExist()
			return [f'This {field} is already taken.']
		except (ValidationError, ValueError):
			return [f'This {field} is either already taken or not available.']
		except ObjectDoesNotExist:
			pass
		return []

def identifyPasswordVulnerabilities(password):
	vulenerabilities = []
	if len(password) < 8:
		vulenerabilities.append('This password is too short.') 
	return vulenerabilities