import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.staticfiles import finders
from app.functions import jsonError

@csrf_exempt
def endpoints(request):
	if request.method != 'GET':
		return jsonError(request, 405, "Method Not Allowed, GET request expected")
	format = request.GET.get('format', None)
	with open(finders.find('json/endpoints.json')) as f:
		json_data = json.load(f)
		return JsonResponse(json_data, safe=False, json_dumps_params={'indent': 2})
	return jsonError(request, 500, 'Resource not available')
