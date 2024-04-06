from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

# ############################################### # 

from api.views.endpoints import endpoints
from api.views.checkAvailability import checkAvailability

from api.views.users import users
from api.views.users_userID import users_userID
from api.views.users_userID_profilePicture import users_userID_profilePicture

from api.views.matchs import matchs
from api.views.ranks import ranks

from api.views.notFound import notFound

urlpatterns = [
	path('', lambda request: redirect('endpoints/')),
	path('endpoints/', endpoints),
    path('check-availability/', checkAvailability),
	path('users/', users),
	path('users/<str:userID>/', users_userID),
	path('users/<str:userID>/profile_picture/', users_userID_profilePicture),
	path('matchs/', matchs),
	path('ranks/', ranks),
    path('<path:remainder>/', notFound)
]
