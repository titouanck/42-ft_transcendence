from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

class getRoutes(APIView):
	permission_classes = [AllowAny]

	def get(self, request, format=None):
		routes = [
			'/api/players/',
			'/api/token/',
			'/api/token/refresh/'
		]
		return Response(routes)
