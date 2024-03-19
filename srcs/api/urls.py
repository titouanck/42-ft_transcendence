from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

# ############################################### # 

from api.views.endpoints import endpoints
from api.views.check_availability import check_availability

urlpatterns = [
	path('', lambda request: redirect('endpoints/')),
	path('endpoints/', endpoints),
    path('check_availability/', check_availability),
]

from api.views.users.data import data
from api.views.users.update import update

users = [
	path('users/<str:userID>/', data),
	path('users/<str:userID>/update/', update),
]
urlpatterns.extend(users)

from api.views.default import defaultAPIView

urlpatterns.append(path('<path:remainder>/', defaultAPIView))
