from django.utils import timezone
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from django.core.exceptions import ValidationError
from .permissions import IsNotAuthenticated

from . import utils
from django.contrib.auth.models import User
from app.models.choices import IN_PROGRESS, COMPLETED
from app.models.Player import Player
from app.models.EmailVerification import EmailVerification
from app.serializers import PlayerSerializer

class getRoutes(APIView):
	permission_classes = [AllowAny]

	def get(self, request, format=None):
		routes = [
			'/api/players/',
			'/api/token/',
			'/api/token/refresh/'
		]
		return Response(routes)

class getPlayers(generics.ListAPIView):
	permission_classes = [AllowAny]
	serializer_class = PlayerSerializer

	def get_queryset(self):
		queryset = Player.objects.all()

		query_params = self.request.query_params.copy()
		
		if 'username' in query_params:
			query_params['user__username'] = query_params['username']
			query_params.pop('username')

		if 'email' in query_params:
			if self.scope() == 'private':
				query_params['user__email'] = query_params['email']
			query_params.pop('email')

		queryset = utils.filter(queryset, query_params)
		return queryset
	
	def get_serializer_context(self):
		context = super().get_serializer_context()
		context.update({"scope": self.scope()})
		return context
	
	def post(self, request, format=None):
		errors = {}

		username = request.data.get('username', None)
		if username is None:
			errors['username'] = ['This field is required.']
		elif not username:
			errors['username'] = ['This field may not be blank.']
		try:
			users = User.objects.get(username=username)
			errors['username'] = ['This username is already taken.']
		except Exception:
			pass
		
		email = request.data.get('email', None)
		if email is None:
			errors['email'] = ['This field is required.']
		elif not email:
			errors['email'] = ['This field may not be blank.']
		elif not utils.isEmailValid(email):
			errors['email'] = ['This email is not valid.']
		try:
			users = User.objects.get(email=email)
			errors['email'] = ['This email is already taken.']
		except Exception:
			pass
		
		password = request.data.get('password', None)
		if password is None:
			errors['password'] = ['This field is required.']
		elif not password:
			errors['password'] = ['This field may not be blank.']
		else:
			password_vulnerabilities = utils.identifyPasswordVulnerabilities(password)
			if password_vulnerabilities:
				errors['password'] = password_vulnerabilities
		
		if errors:
			return Response(errors, status=status.HTTP_400_BAD_REQUEST)
		
		try:
			new_user = User.objects.create_user(username, email, password)
			new_player = Player.objects.create(user=new_user)
			serializer = PlayerSerializer(new_player, context={'scope' : 'private'})
			return Response(serializer.data)
		except Exception as e:
			return Response({'detail' : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

	def scope(self):
		return self.request.query_params.get('scope', None)

class getPlayer(APIView):
	permission_classes = [AllowAny]

	def get(self, request, player, format=None):
		player_object = self.retrieve_player(player)
		serializer = PlayerSerializer(player_object, context={'scope' : self.scope()})
		return Response(serializer.data)
	
	def patch(self, request, player, format=None):
		player_object = self.retrieve_player(player)
		serializer = PlayerSerializer(player_object, data=request.data, partial=True, context={'scope' : self.scope()})
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def scope(self):
		return self.request.query_params.get('scope', None)
	
	def retrieve_player(self, player):
		try:
			player_object = Player.objects.get(pk=player)
		except ValidationError:
			try:
				user_object = User.objects.get(username=player)
				player_object = Player.objects.get(user=user_object.id)
			except (User.DoesNotExist, Player.DoesNotExist) as e:
				return Response({'detail' : str(e)}, status=status.HTTP_404_NOT_FOUND)
			except ValidationError as e:
				raise e
		return player_object

class verify(APIView):
	permission_classes = [IsAuthenticated]

	def post(self, request, format=None):
		errors = {}

		slug = request.data.get('slug', None)
		if slug is None:
			errors['slug'] = ['This field is required.']
		elif not slug:
			errors['slug'] = ['This field may not be blank.']
		else:
			try:
				email_verification = EmailVerification.objects.get(verification_slug=slug)
			except (EmailVerification.DoesNotExist, ValidationError, ValueError):
				errors['slug'] = ['This slug is not valid.']

		if errors:
			return Response(errors, status=status.HTTP_400_BAD_REQUEST)
		
		if not email_verification.is_valid():
			return Response({"detail": "This link has expired."}, status=419)
		if email_verification.user != request.user:
			return Response({"detail": "This is not the good account."},  status=status.HTTP_403_FORBIDDEN)
		
		try:
			User.objects.get(email=email_verification.email)
			return Response({"detail" : "This email is already taken."}, status=status.HTTP_400_BAD_REQUEST)
		except Exception as e:
			pass
		
		player = Player.objects.get(user=request.user)
		if not player.set_email(email_verification.email):
			return Response({"detail" : "Could not save email."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

		email_verification.verification_status = COMPLETED
		email_verification.save()
		serializer = PlayerSerializer(player, context={'scope' : 'private'})
		return Response(serializer.data)
