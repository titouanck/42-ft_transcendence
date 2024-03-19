from django.utils import timezone
from django.http import JsonResponse
import re

from app.models import Player, Pongtoken

def is_slug(s):
    pattern = r'^[a-z0-9]+(?:-[a-z0-9]+)*$'
    return re.match(pattern, s) is not None

def is_username_available(username):
	print(f'|{username}|')
	if username:
		username = username.lower()
		try:
			Player.objects.get(username=username)
		except Exception as e:
			if len(username) >= 1 and len(username) <= 12 and is_slug(username):
				return True
	return False

def is_email_available(email):
	if email:
		try:
			Player.objects.get(email=email)
		except Exception as e:
			regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
			if re.match(regex, email):
				return True
	return False

def check_token(cookie):
	try:
		pongtoken_obj = Pongtoken.objects.get(pk=cookie)
		if timezone.now() < pongtoken_obj.expires_at:
			return True
	except Exception as e:
		pass
	return False

def jsonError(request, code, message):
	data = {
		'error' : code,
		'message' : message,
		'documentation_url' : f'{request.scheme}://{request.get_host()}/api/endpoints'
	}
	return JsonResponse(data, status=code, json_dumps_params={'indent': 2})
