from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User
from app.models.choices import COMPLETED
from app.models.Player import Player
from app.models.EmailVerification import EmailVerification
from app.serializers.PlayerSerializer import PlayerSerializer

class confirmEmail(APIView):
	permission_classes = [IsAuthenticated]

	def post(self, request, verification_slug, format=None):
		errors = {}

		try:
			email_verification = EmailVerification.objects.get(verification_link=verification_slug)
			if not email_verification.is_valid():
				raise ValidationError(None)
		except (EmailVerification.DoesNotExist, ValidationError, ValueError):
			return Response({"detail": "This email verification link has expired."}, status=status.HTTP_410_GONE)

		if email_verification.user != request.user:
			return Response({"detail": "You are connected from a different account."},  status=status.HTTP_403_FORBIDDEN)
		
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
