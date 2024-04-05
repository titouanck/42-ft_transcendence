import os
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
from api.functions import retrieveUserIDs
from app.functions import jsonError, formatValidationErrorMessage
from django.utils import timezone

@csrf_exempt
def users_userID_image(request, userID):
	if request.method == 'GET':
		return _GET(request, userID)
	if request.method == 'POST':
		return _POST(request, userID)
	else:
		return jsonError(request, 405, "Method Not Allowed")

def _GET(request, userID):
	status, content = retrieveUserIDs(request, userID)
	if not status:
		return content
	requester = content['requester']
	target = content['target']

	image_data = target.image.read()
	image_extension = target.image_url[len('local.'):]
	image_name = f'{target.username}_{target.uid}'
	
	response = HttpResponse(image_data, content_type=f"image/{image_extension}")
	response['Content-Disposition'] = f'inline; filename="{image_name}.{image_extension}"'
    
	return response

def _POST(request, userID):
	status, content = retrieveUserIDs(request, userID)
	if not status:
		return content
	requester = content['requester']
	target = content['target']
	if requester and (requester != target and requester.operator is False):
		return jsonError(request, 403, 'Forbidden, not enough permissions')
	
	response = {
		"updated_fields": [],
	}

	uploadedImage = request.FILES['image']
	if uploadedImage:
		try:
			target.upload_image(uploadedImage)
		except Exception as e:
			return jsonError(request, 400, formatValidationErrorMessage(e))
	return JsonResponse(response, status=200, json_dumps_params={'indent': 2})
