import json
from django.http import JsonResponse
from app.models import Player, Pongtoken
from django.views.decorators.csrf import csrf_exempt
from django.contrib.staticfiles import finders
import app.functions as func
from app.functions import jsonError

@csrf_exempt
def data(request, userID):
	if request.method != 'GET':
		return jsonError(request, 405, "Method Not Allowed, GET request expected")
	access_token = request.headers.get('Authorization')
	if access_token:
		try:
			access_token = access_token.split()[1]
			pongtoken = Pongtoken.objects.get(pk=access_token)
		except IndexError:
			return jsonError(request, 401, 'Malformed authorization token')
		except Pongtoken.DoesNotExist:
			return jsonError(request, 401, 'Invalid authorization token')
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
		except Exception as e:
			return jsonError(request, 500, 'Internal server error')

	response = {
		'uid' : user.uid,
		'username' : user.username,
		'status' : user.status,
		'pic' : user.pic,
		'rank' : user.rank,
		'elo' : user.elo,
		'victories' : user.victories,
		'defeats' : user.defeats,
	}
	
	if pongtoken and pongtoken.user.admin:
		response['admin'] = user.admin
		response['email'] = user.email
		response['login_42'] = user.login_42
		response['created_at'] = user.created_at
		response['updated_at'] = user.updated_at

	return JsonResponse(response, response=200, json_dumps_params={'indent': 2})
