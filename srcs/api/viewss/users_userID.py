import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from api.functions import retrieveUserIDs
from app.functions import jsonError, isUsernameAvailable, isEmailAvailable

@csrf_exempt
def users_userID(request, userID):
	if request.method == 'GET':
		return _GET(request, userID)
	elif request.method == 'PATCH':
		return _PATCH(request, userID)
	else:
		return jsonError(request, 405, "Method Not Allowed")
		
def _GET(request, userID):
	status, content = retrieveUserIDs(request, userID)
	if not status:
		return content
	requester = content['requester']
	target = content['target']

	if requester and (requester == target or requester.operator is True):
		response = target.privateData(request)
	else:
		response = target.publicData(request)
	return JsonResponse(response, status=200, json_dumps_params={'indent': 2})

def _PATCH(request, userID):
	status, content = retrieveUserIDs(request, userID)
	if not status:
		return content
	requester = content['requester']
	target = content['target']
	if requester and (requester != target and requester.operator is False):
		return jsonError(request, 403, 'Forbidden, not enough permissions')

	try:
		data = json.loads(request.body.decode('utf-8'))
	except json.decoder.JSONDecodeError:
		return jsonError(request, 400, 'JSON body required')
	except Exception as e:
		return jsonError(request, 500, 'Internal server error')
	
	response = {
		"updated_fields": [],
	}

	username = data.get('username', None)
	if username:
		username = username.lower().strip()
		if username != target.username and isUsernameAvailable(username):
			target.username = username
			response["updated_fields"].append("username")
	
	email = data.get('email', None)
	if email:
		if email != target.email and isEmailAvailable(email):
			target.email = email
			response["updated_fields"].append("email")
	
	target.save()
	return JsonResponse(response, status=200, json_dumps_params={'indent': 2})
