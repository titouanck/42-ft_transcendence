from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import app.functions as func
from app.functions import jsonError

@csrf_exempt
def checkAvailability(request):
	if request.method != 'GET':
		return jsonError(request, 405, "Method Not Allowed")
	
	dict = {}
	username = request.GET.get('username', None)
	if username:
		dict['username_available'] = func.isUsernameAvailable(username)
	email = request.GET.get('email', None)
	if email:
		dict['email_available'] = func.isEmailAvailable(email)
	return JsonResponse(dict, json_dumps_params={'indent': 2})