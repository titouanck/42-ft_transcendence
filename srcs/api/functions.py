from app.models import Player, Pongtoken
from django.core.exceptions import ValidationError
import app.functions as func
from app.functions import jsonError, formatValidationErrorMessage

def getQueryParams(queryDict):
	queryParams = {}
	for key in queryDict:
		queryParams[key] = queryDict[key].split(',')
		for i, param in enumerate(queryParams[key]):
			queryParams[key][i] = param.lstrip()
	return queryParams

def	retrieveUserIDs(request, userID):
	requester = None
	target = None

	access_token = request.headers.get('Authorization')
	if access_token:
		try:
			access_token = access_token.split()[1]
			pongtoken = Pongtoken.objects.get(pk=access_token)
		except IndexError:
			return False, jsonError(request, 401, 'Malformed authorization token')
		except Pongtoken.DoesNotExist:
			return False, jsonError(request, 401, 'Invalid authorization token')
		except Player.DoesNotExist:
			return False, jsonError(request, 404, 'Resource not found')
		except ValidationError as e:
			return False, jsonError(request, 400, formatValidationErrorMessage(e))
		except Exception as e:
			return False, jsonError(request, 500, 'Internal server error')
	elif request.COOKIES and 'pongtoken' in request.COOKIES and func.checkToken(request.COOKIES['pongtoken']):
		pongtoken = Pongtoken.objects.get(pk=request.COOKIES['pongtoken'])
	else:
		pongtoken = None

	if pongtoken:
		requester = pongtoken.user
	
	if userID == "me":
		if pongtoken:
			target = pongtoken.user
		else:
			return False, jsonError(request, 401, 'Requires authentication: missing authorization token')
	else:
		try:
			target = Player.objects.get(pk=userID)
		except Player.DoesNotExist:
			return False, jsonError(request, 404, 'Resource not found')
		except ValidationError as e:
			try:
				target = Player.objects.get(username=userID)
			except Exception as error:
				return False, jsonError(request, 400, f'{userID} is not a valid UUID, username or keyword')
		except Exception as e:
			return False, jsonError(request, 500, 'Internal server error')
		
	return True, {'requester':requester, 'target':target}