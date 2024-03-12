import os, requests, json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from urllib.parse import urlencode
from datetime import datetime
from .models import FortyTwoToken, Player

def is_token_valid(cookie):
	try:
		fortytwotoken_obj = FortyTwoToken.objects.get(pk=cookie)
		Player.objects.get(token_42=fortytwotoken_obj)
		print(f'current time : {timezone.now()}')
		print(f'expires at : {fortytwotoken_obj.expires_at}')
		if timezone.now() < fortytwotoken_obj.expires_at:
			return True
		else:
			print('is_token_valid returns else')
	except Exception as e:
		pass
	return False

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

def acquire_access_token(code):
	url = 'https://api.intra.42.fr/oauth/token'
	params = {
		'grant_type' : 'authorization_code',
		'client_id' : os.environ['CLIENT_ID'],
		'client_secret' : os.environ['CLIENT_SECRET'],
		'code' : code,
		'redirect_uri' : 'http://127.0.0.1:8000/api',
	}
	response = requests.post(url, json = params)
	if response.status_code != 200:
		print(f'acquire_access_token: Error {response.status_code}')
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

def save_new_token(code):
	token_json = acquire_access_token(code)
	if token_json is None or 'access_token' not in token_json:
		return None
	login, image = fetch_user_data(token_json['access_token'])
	obj = FortyTwoToken()
	if 'secret_valid_until' in token_json:
		obj.expires_at = datetime.fromtimestamp(int(token_json['secret_valid_until']))
	else:
		obj.expires_at = timezone.now() + timezone.timedelta(days=7)
	obj.save()
	try:
		player = Player.objects.get(login_42=login)
	except Player.DoesNotExist:
		player = Player()
		player.login_42 = login
		player.pic = image
	player.token_42 = obj
	player.save()
	print(f'value: {obj.uid}, expires: {obj.expires_at}')
	return {'value' : obj.uid, 'expires' : obj.expires_at}

def auth(request):
	if request.COOKIES and 'fortytwotoken' in request.COOKIES and is_token_valid(request.COOKIES['fortytwotoken']):
		fortytwotoken_obj = FortyTwoToken.objects.get(pk=request.COOKIES['fortytwotoken'])
		player = Player.objects.get(token_42=fortytwotoken_obj)
		return render(request, 'profil.html', {'username' : player.login_42, 'pic' : player.pic})
	auth_method = request.GET.get('auth_method', None)
	code = request.GET.get('code', None)
	if auth_method !='fortytwo' and not code:
		return render(request, 'auth.html')
	if code is None or not code:
		return request_42_access()
	cookie = save_new_token(code)
	if cookie is None:
		return HttpResponse('Big problem')
	response = redirect(request.path)
	response.set_cookie('fortytwotoken', value=cookie['value'], expires=cookie['expires'])
	return response

def auth_page(request):
	return render(request, 'auth.html')