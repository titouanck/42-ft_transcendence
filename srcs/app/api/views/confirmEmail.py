from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User
from app.models.choices import COMPLETED
from app.models.Player import Player
from app.models.EmailVerification import EmailVerification
from app.serializers import PlayerSerializer

class confirmEmail(APIView):
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
			return Response({"detail": "You are connected from."},  status=status.HTTP_403_FORBIDDEN)
		
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
