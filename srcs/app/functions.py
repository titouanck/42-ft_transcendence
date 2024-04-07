# from django.utils import timezone
# from django.http import JsonResponse
# import re

# from app.models.Player import Player
# from app.models.Pongtoken import Pongtoken

# def isSlug(s):
#     pattern = r'^[a-z0-9]+(?:-[a-z0-9]+)*$'
#     return re.match(pattern, s) is not None

# def isUsernameAvailable(username):
# 	if username:
# 		username = username.lower()
# 		try:
# 			Player.objects.get(username=username)
# 		except Exception as e:
# 			if len(username) >= 1 and len(username) <= 12 and isSlug(username):
# 				return True
# 	return False

# def isEmailAvailable(email):
# 	if email:
# 		try:
# 			Player.objects.get(email=email)
# 		except Exception as e:
# 			regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
# 			if re.match(regex, email):
# 				return True
# 	return False

# def checkToken(pongtoken_uid):
# 	try:
# 		pongtoken_obj = Pongtoken.objects.get(pk=pongtoken_uid)
# 		return not pongtoken_obj.is_expired()
# 	except Exception as e:
# 		pass
# 	return False

# def jsonError(request, code, message):
# 	data = {
# 		'error' : code,
# 		'message' : message,
# 		'documentation_url' : f'{request.scheme}://{request.get_host()}/api/endpoints/'
# 	}
# 	return JsonResponse(data, status=code, json_dumps_params={'indent': 2})

# def formatValidationErrorMessage(e):
# 	s = str(e).replace("'", '').replace('“', "").replace('”', "")
# 	if len(s) <= 2:
# 		return s
# 	else:
# 		return s[1:-1]