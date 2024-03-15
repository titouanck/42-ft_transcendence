import os, requests, json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from urllib.parse import urlencode
from datetime import datetime
from app.models import Player, Pongtoken
from django.views.decorators.csrf import csrf_exempt
import re

def is_slug(s):
    pattern = r'^[a-z0-9]+(?:-[a-z0-9]+)*$'
    return re.match(pattern, s) is not None

def is_username_available(username):
	print(f'|{username}|')
	if username:
		username = username.lower()
		try:
			Player.objects.get(username=username)
		except Exception as e:
			if len(username) >= 1 and len(username) <= 12 and is_slug(username):
				return True
	return False

def is_email_available(email):
	if email:
		try:
			Player.objects.get(email=email)
		except Exception as e:
			regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
			if re.match(regex, email):
				return True
	return False

@csrf_exempt
def check_availability(request):
	dict = {}
	username = request.GET.get('username', None)
	if username:
		dict['username-available'] = is_username_available(username)
	email = request.GET.get('email', None)
	if email:
		dict['email-available'] = is_email_available(email)
	return  JsonResponse(dict)

@csrf_exempt
def change_user_info(request):
	pongtoken = request.POST.get('access_token', None)
	try:
		pongtoken_obj = Pongtoken.objects.get(pk=pongtoken)
		user = Player.objects.get(pongtoken=pongtoken_obj)
	except Pongtoken.DoesNotExist or Player.DoesNotExist:
		return JsonResponse({'error': f'Missing or invalid token {pongtoken}, who are you?'}, status=403)
	username = request.POST.get('username', None)
	if username:
		username = username.lower().strip()
		if username != user.username and not is_username_available(username):
			return JsonResponse({'error': f'Conflict: username {username} not available'}, status=409)
		user.username = username
		user.save()
		return JsonResponse({'changed' : 'username'}, status=200)
	email = request.POST.get('email', None)
	if email:
		if email != user.email and not is_email_available(email):
			return JsonResponse({'error': f'Conflict: email {email} not available'}, status=409)
		user.email = email
		user.save()
		return JsonResponse({'changed' : 'email'}, status=200)
	return JsonResponse({'changed' : ''}, status=200)
