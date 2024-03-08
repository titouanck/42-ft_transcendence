import os, random, requests, json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from urllib.parse import urlencode
from datetime import datetime, timedelta
from .models import FortyTwoToken

def request_42_access():
	url = 'https://api.intra.42.fr/oauth/authorize'
	params = {
		'client_id' : os.environ['CLIENT_ID'],
		'redirect_uri' : 'http://127.0.0.1:8000/api',
		'scope' : 'public',
		'response_type' : 'code',
	}
	redirect_url = f'{url}?{urlencode(params)}'
	return redirect(redirect_url)

def acquire_access_token(code=None, refresh_token=None):
	url = 'https://api.intra.42.fr/oauth/token'
	params = {
		'grant_type' : 'authorization_code',
		'client_id' : os.environ['CLIENT_ID'],
		'client_secret' : os.environ['CLIENT_SECRET'],
		'code' : code,
		'redirect_uri' : 'http://127.0.0.1:8000/api',
	}
	if code:
		params['grant_type'] = 'authorization_code'
		params['code'] = code
	elif refresh_token:
		params['grant_type'] = 'refresh_token'
		params['refresh_token'] = refresh_token
	else:
		return None
	response = requests.post(url, json = params)
	if response.status_code != 200:
		return None
	return json.loads(response.content)

def fetch_user_data(access_token):
	url = 'https://api.intra.42.fr/v2/me'
	headers = {
		'Authorization' : f'Bearer {access_token}'
	}
	response = requests.get(url, headers = headers)
	if response.status_code != 200:
		return None
	response_json = json.loads(response.content)
	login = response_json.get('login', None)
	image = response_json.get('image', {}).get('link', None)
	return login, image

# 1. FALSE SI PROBLEME, TRUE SI RIEN A FAIRE, COOKIE SINON
# Create your views here.

def is_token_valid(cookies):
	if cookies is None or 'fortytwotoken' not in cookies:
		print('first return')
		return False
	try:
		fortytwotoken_obj = FortyTwoToken.objects.get(pk=cookies['fortytwotoken'])
		if timezone.now() < fortytwotoken_obj.access_expires_at:
			print('1.5 return')
			return True
		elif timezone.now() < fortytwotoken_obj.secret_expires_at and fortytwotoken_obj.refresh_token:
			token_json = acquire_access_token(refresh_token=fortytwotoken_obj.refresh_token)
			if token_json and 'access_token' in token_json:
				fortytwotoken_obj.access_token = token_json
				if 'expires_in' in token_json:
					fortytwotoken_obj.access_expires_at = timezone.now() + datetime.fromtimestamp(int(token_json['expires_in']))
				print('second return')
				return True
		fortytwotoken_obj.delete()
	except FortyTwoToken.DoesNotExist:
		pass
	print('third return')
	return False

def generate_new_token(code):
	token_json = acquire_access_token(code=code)
	if token_json is None or 'access_token' not in token_json:
		return None
	login, image = fetch_user_data(token_json['access_token'])
	obj = FortyTwoToken()
	obj.access_token = token_json['access_token']
	obj.refresh_token = token_json.get('refresh_token', None)
	obj.login = login
	if 'created_at' in token_json and 'expires_in' in token_json:
		obj.access_expires_at = timezone.make_aware(datetime.fromtimestamp(int(token_json['created_at']) + int(token_json['expires_in'])))
	if 'secret_valid_until' in token_json:
		expires = datetime.fromtimestamp(int(int(token_json['secret_valid_until'])))
		obj.secret_expires_at = expires
	obj.save()
	return {'name' : 'fortytwotoken', 'value' : obj.uid, 'expires' : obj.secret_expires_at}

def auth(request):
	if is_token_valid(request.COOKIES):
		return HttpResponse('TOKEN VALID')
	code = request.GET.get('code', None)
	if code is None or not code:
		return request_42_access()
	result = generate_new_token(code)
	response = HttpResponse('Successfully acquired access token')
	response.set_cookie(result['name'], value=result['value'], expires=result.get('expires'))
	return response

def me(request):
	if 'fortytwotoken' in request.COOKIES:
		obj = FortyTwoToken.objects.get(pk=request.COOKIES['fortytwotoken'])
		return render(request, 'me.html', {'login' : obj.login})
	return render(request, 'me.html')
	