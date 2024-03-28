import os, requests, json
from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import datetime
from .models import Pongtoken, Player
import app.functions as func

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
	pongtoken = Pongtoken()
	if 'secret_valid_until' in token_json:
		pongtoken.expires_at = datetime.fromtimestamp(int(token_json['secret_valid_until']))
	else:
		pongtoken.expires_at = timezone.now() + timezone.timedelta(days=7)
	try:
		player = Player.objects.get(login_42=login)
	except Player.DoesNotExist:
		player = Player()
		player.login_42 = login
		player.username = login
		player.image = image
		player.save()
	pongtoken.user = player
	pongtoken.save()
	return True, {'value' : pongtoken.uid, 'expires' : pongtoken.expires_at}

def main_app(request):
	code = request.GET.get('code', None)
	if not code:
		if request.COOKIES and 'pongtoken' in request.COOKIES and func.checkToken(request.COOKIES['pongtoken']):
			pongtoken = Pongtoken.objects.get(pk=request.COOKIES['pongtoken'])
			player = pongtoken.user
			return render(request, 'index.html', {'connected' : True, "profile_pic" : player.image, "username" : player.username, "rank" : f'img/rank-{player.rank.lower()}.png'})
		else:
			return render(request, 'index.html', {'not_connected' : True})
	status, cookie = save_new_token(code, request.build_absolute_uri(request.path))
	if status is False:
		return render(request, 'index.html', {'not_connected' : True, 'alert_message' : cookie})
	response = redirect(request.path)
	response.set_cookie('pongtoken', value=cookie['value'], expires=cookie['expires'])
	return response

def websockets(request):
	return render(request, 'ws.html')
