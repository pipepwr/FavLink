from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from rest_framework.response import Response
from rest_framework import status

from rest_framework.views import APIView

from rest_api.serializers import UserSerializer


class UserView(APIView):
    """
    API endpoint that allows users to be viewed or edited.
    """

    def post(self, request):
        """
        Post Route
        Must Have [username, password]
        username must unique
        password validate by password hasher in settings
        """

        user_serializer = UserSerializer(data=request.data)

        if user_serializer.is_valid():
            user_name = request.data.get("username")
            email = request.data.get("email")
            password = request.data.get("password")

            try:
                validate_password(password)
            except ValidationError as e:
                error_messages = list(e.messages)
                return Response(
                    {"Password Check": error_messages},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user = User.objects.create_user(
                username=user_name, email=email, password=password
            )
            user.save()
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
