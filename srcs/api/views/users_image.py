import os
import json
from django.http import JsonResponse, HttpResponse
from app.models import Player, Pongtoken
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from app.functions import jsonError, formatValidationErrorMessage
from PIL import Image

@csrf_exempt
def users_image(request, userID):
	if request.method == 'GET':
		return users_image_GET(request, userID)
	if request.method == 'POST':
		return users_image_POST(request, userID)
	else:
		return jsonError(request, 405, "Method Not Allowed")

def users_image_GET(request, userID):
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


	image_data = user.image.read()
	image_extension = user.image_url[len('local.'):]
	image_name = f'{user.username}_{user.uid}'
	
	response = HttpResponse(image_data, content_type=f"image/{image_extension}")
	response['Content-Disposition'] = f'inline; filename="{image_name}.{image_extension}"'
    
	return response

def users_image_POST(request, userID):
	
	try:
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

	print(request.FILES)
	uploaded_image = request.FILES['image']
	if uploaded_image:
		try:
			img = Image.open(uploaded_image)
			img.verify()
			original_filename, original_extension = os.path.splitext(uploaded_image.name)
			new_filename = f'{user.uid}{original_extension}'
			user.image_url = f'local{original_extension}'
			user.image.delete()
			user.image.save(new_filename, uploaded_image)
			response["updated_fields"].append("image")
			response["updated_fields"].append("image_url")
		except Exception as e:
			return jsonError(request, 400, formatValidationErrorMessage(e))
	return JsonResponse(response, status=200, json_dumps_params={'indent': 2})
