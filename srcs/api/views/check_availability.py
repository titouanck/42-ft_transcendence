from django.http import JsonResponse
from app.models import Player
from django.views.decorators.csrf import csrf_exempt
import re
import app.functions as func
from app.functions import jsonError

@csrf_exempt
def check_availability(request):
	if request.method != 'GET':
		return jsonError(request, 405, "Method Not Allowed, GET request expected")
	dict = {}
	username = request.GET.get('username', None)
	if username:
		dict['username_available'] = func.is_username_available(username)
	email = request.GET.get('email', None)
	if email:
		dict['email_available'] = func.is_email_available(email)
	return  JsonResponse(dict, json_dumps_params={'indent': 2})