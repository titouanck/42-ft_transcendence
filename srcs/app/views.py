import os, requests, json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from urllib.parse import urlencode
from datetime import datetime
from .models import Pongtoken, Player

def is_token_valid(cookie):
	try:
		pongtoken_obj = Pongtoken.objects.get(pk=cookie)
		Player.objects.get(pongtoken=pongtoken_obj)
		print(f'current time : {timezone.now()}')
		print(f'expires at : {pongtoken_obj.expires_at}')
		if timezone.now() < pongtoken_obj.expires_at:
			return True
	except Exception as e:
		pass
	return False

def acquire_access_token(code, redirect_uri):
	url = 'https://api.intra.42.fr/oauth/token'
	params = {
		'grant_type' : 'authorization_code',
		'client_id' : os.environ['CLIENT_ID'],
		'client_secret' : os.environ['CLIENT_SECRET'],
		'code' : code,
		'redirect_uri' : redirect_uri,
	}
	response = requests.post(url, json = params)
	if response.status_code != 200:
		print(response.content)
		return response.status_code, None
	return response.status_code, json.loads(response.content)

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

def save_new_token(code, redirect_uri):
	status, token_json = acquire_access_token(code, redirect_uri)
	if status != 200:
		return False, f"Error {status} returned by the 42 api"
	elif 'access_token' not in token_json:
		return False, "Missing access_token in response from the 42 api"
	login, image = fetch_user_data(token_json['access_token'])
	obj = Pongtoken()
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
		player.username = login
		player.pic = image
	player.pongtoken = obj
	player.save()
	print(f'value: {obj.uid}, expires: {obj.expires_at}')
	return True, {'value' : obj.uid, 'expires' : obj.expires_at}

def main_app(request):
	code = request.GET.get('code', None)
	if not code:
		if request.COOKIES and 'pongtoken' in request.COOKIES and is_token_valid(request.COOKIES['pongtoken']):
			pongtoken_obj = Pongtoken.objects.get(pk=request.COOKIES['pongtoken'])
			player = Player.objects.get(pongtoken=pongtoken_obj)
			print("yoo" + player.rank)
			return render(request, 'topbar.html', {'connected' : True, "profile_pic" : player.pic, "username" : player.username, "rank" : f'img/rank-{player.rank.lower()}.png'})
		else:
			return render(request, 'topbar.html', {'not_connected' : True})
	status, cookie = save_new_token(code, request.build_absolute_uri(request.path))
	if status is False:
		return render(request, 'topbar.html', {'not_connected' : True, 'alert_message' : cookie})
	response = redirect(request.path)
	response.set_cookie('pongtoken', value=cookie['value'], expires=cookie['expires'])
	return response
