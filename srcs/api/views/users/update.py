import json
from django.http import JsonResponse
from app.models import Player, Pongtoken
from django.views.decorators.csrf import csrf_exempt
from django.contrib.staticfiles import finders
import app.functions as func
from app.functions import jsonError

@csrf_exempt
def update(request, userID):
	if request.method != 'POST':
		return jsonError(request, 405, "Method Not Allowed, POST request expected")
	try:
		access_token = request.headers.get('Authorization')
		if not access_token:
			return jsonError(request, 401, 'Requires authentication: missing authorization token')
		access_token = access_token.split()[1]
		pongtoken = Pongtoken.objects.get(pk=access_token)
		if userID == "me" or userID == pongtoken.user.uid:
			user = pongtoken.user
		elif pongtoken.user.admin:
			try:
				user = Player.objects.get(pk=userID)
			except Player.DoesNotExist:
				return jsonError(request, 404, 'Resource not found')
		else:
			return jsonError(request, 403, 'Forbidden, not enough permissions')
	except IndexError:
		return jsonError(request, 401, 'Malformed authorization token')
	except Pongtoken.DoesNotExist:
		return jsonError(request, 401, 'Invalid authorization token')
	except Exception as e:
		return jsonError(request, 500, 'Internal server error')

	try:
		pongtoken = Pongtoken.objects.get(pk=access_token)
		if userID == "me" or userID == pongtoken.user.uid:
			user = pongtoken.user
		elif pongtoken.user.admin == False:
			return jsonError(request, 403, 'Forbidden, not enough permissions')
		else:
			try:
				user = Player.objects.get(pk=userID)
			except Exception as e:
				return jsonError(request, 404, 'Resource not found')
	except Exception as e:
		return jsonError(request, 401, 'Missing or invalid token, who are you?')
	
	response = {
		"updated": []
	}

	username = request.POST.get('username', None)
	if username:
		username = username.lower().strip()
		if username != user.username and func.is_username_available(username):
			user.username = username
			response["updated"].append("username")
	
	email = request.POST.get('email', None)
	if email:
		if email != user.email and func.is_email_available(email):
			user.email = email
			response["updated"].append("email")

	user.save()
	return JsonResponse(response, status=200, json_dumps_params={'indent': 2})
