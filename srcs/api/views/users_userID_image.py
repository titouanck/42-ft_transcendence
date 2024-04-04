import os
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
from api.functions import retrieveUserIDs
from app.functions import jsonError, formatValidationErrorMessage

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

	uploaded_image = request.FILES['image']
	if uploaded_image:
		try:
			img = Image.open(uploaded_image)
			img.verify()
			original_filename, original_extension = os.path.splitext(uploaded_image.name)
			new_filename = f'{target.uid}{original_extension}'
			target.image_url = f'local{original_extension}'
			target.image.delete()
			target.image.save(new_filename, uploaded_image)
			response["updated_fields"].append("image")
			response["updated_fields"].append("image_url")
		except Exception as e:
			return jsonError(request, 400, formatValidationErrorMessage(e))
	return JsonResponse(response, status=200, json_dumps_params={'indent': 2})
