from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

# ############################################### # 

from api.views.endpoints import endpoints
from api.views.check_availability import check_availability
from api.views.users import users
from api.views.notFound import notFound

urlpatterns = [
	path('', lambda request: redirect('endpoints/')),
	path('endpoints/', endpoints),
    path('check_availability/', check_availability),
	path('users/<str:userID>/', users),
    path('<path:remainder>/', notFound)
]
