from django.db.models import Q
from django.core.exceptions import FieldError, ValidationError
import re

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

# def formatMessageValidationError(e):
# 	s = str(e).replace("'", '').replace('“', "").replace('”', "")
# 	if len(s) <= 2:
# 		return s
# 	else:
# 		return s[1:-1]

def isEmailValid(email):
	regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
	if re.match(regex, email):
		return True
	return False

def identifyPasswordVulnerabilities(password):
	vulenerabilities = []
	if len(password) < 8:
		vulenerabilities.append('This password is too short.') 
	return vulenerabilities

