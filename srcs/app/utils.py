from django.conf import settings
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.exceptions import FieldError, ValidationError, ObjectDoesNotExist
from rest_framework.permissions import BasePermission, SAFE_METHODS
import os
import re
import secrets
import string

class IsNotAuthenticated(BasePermission):
	def has_permission(self, request, view):
		return not request.user or not request.user.is_authenticated
	
class IsNotAuthenticatedOrReadOnly(BasePermission):
	def has_permission(self, request, view):
		if request.method in SAFE_METHODS or not request.user or not request.user.is_authenticated:
			return True
		return False

def filter(queryset, query_params):
	for field_name, field_value in query_params.items():
		try:
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
		except Exception:
			continue
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

def readStaticFile(file_path):
	static_path = settings.STATICFILES_DIRS[0]
	full_path = os.path.join(static_path, file_path)
	content = None
	with open(full_path, 'r') as file:
		content = file.read()
	return content


def replaceVars(string, dictionary):
    def replace_variable(match):
        variable = match.group(1)
        return dictionary.get(variable, match.group(0))

    import re
    pattern = r'\${([^}]*)}'
    new_string = re.sub(pattern, replace_variable, string)
    return new_string

def randomSlug(number):
	slug = ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(number))
	return slug