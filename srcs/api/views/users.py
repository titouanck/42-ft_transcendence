import requests
import json
from django.http import JsonResponse
from app.models import Player, Pongtoken
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
import app.functions as func
from app.functions import jsonError, formatValidationErrorMessage
from PIL import Image

@csrf_exempt
def users(request, userID):
	if request.method == 'GET':
		return users_GET(request, userID)
	elif request.method == 'PATCH':
		return users_PATCH(request, userID)
	else:
		return jsonError(request, 405, "Method Not Allowed")


def users_GET(request, userID):
	access_token = request.headers.get('Authorization')
	if access_token:
		try:
			access_token = access_token.split()[1]
			pongtoken = Pongtoken.objects.get(pk=access_token)
		except IndexError:
			return jsonError(request, 401, 'Malformed authorization token')
		except Pongtoken.DoesNotExist:
			return jsonError(request, 401, 'Invalid authorization token')
		except ValidationError as e:
			return jsonError(request, 400, formatValidationErrorMessage(e))
		except Exception as e:
			return jsonError(request, 500, 'Internal server error')
	else:
		pongtoken = None
	
	if userID == "me":
		if pongtoken:
			user = pongtoken.user
		else:
			return jsonError(request, 401, 'Requires authentication: missing authorization token')
	else:
		try:
			user = Player.objects.get(pk=userID)
		except Player.DoesNotExist:
			return jsonError(request, 404, 'Resource not found')
		except ValidationError as e:
			return jsonError(request, 400, formatValidationErrorMessage(e))
		except Exception as e:
			return jsonError(request, 500, 'Internal server error')

	response = {
		'uid' : user.uid,
		'username' : user.username,
		'status' : user.status,
		'image_url' : user.image_url,
		'rank' : user.rank,
		'elo' : user.elo,
		'victories' : user.victories,
		'defeats' : user.defeats,
	}

	if response['image_url'].startswith('local.'):
		response['image_url'] = f'{request.scheme}://{request.get_host()}/api/users/{user.uid}/image/'
	
	if pongtoken and (pongtoken.user.operator or pongtoken.user == user):
		response['operator'] = user.operator
		response['email'] = user.email
		response['login_42'] = user.login_42
		response['created_at'] = user.created_at
		response['updated_at'] = user.updated_at

	return JsonResponse(response, status=200, json_dumps_params={'indent': 2})


def users_PATCH(request, userID):
	try:
		data = json.loads(request.body.decode('utf-8'))
		access_token = request.headers.get('Authorization')
		if not access_token:
			return jsonError(request, 401, 'Requires authentication: missing authorization token')
		access_token = access_token.split()[1]
		pongtoken = Pongtoken.objects.get(pk=access_token)
		
		if userID == "me" or userID == pongtoken.user.uid:
			user = pongtoken.user
		elif pongtoken.user.operator:
			user = Player.objects.get(pk=userID)
		else:
			return jsonError(request, 403, 'Forbidden, not enough permissions')

	except json.decoder.JSONDecodeError:
		return jsonError(request, 400, 'JSON body required')
	except IndexError:
		return jsonError(request, 401, 'Malformed authorization token')
	except Pongtoken.DoesNotExist:
		return jsonError(request, 401, 'Invalid authorization token')
	except Player.DoesNotExist:
		return jsonError(request, 404, 'Resource not found')
	except ValidationError as e:
		return jsonError(request, 400, formatValidationErrorMessage(e))
	except Exception as e:
		return jsonError(request, 500, 'Internal server error')
	
	response = {
		"updated_fields": [],
	}

	username = data.get('username', None)
	if username:
		username = username.lower().strip()
		if username != user.username and func.isUsernameAvailable(username):
			user.username = username
			response["updated_fields"].append("username")
	
	email = data.get('email', None)
	if email:
		if email != user.email and func.isEmailAvailable(email):
			user.email = email
			response["updated_fields"].append("email")
	
	user.save()
	return JsonResponse(response, status=200, json_dumps_params={'indent': 2})
