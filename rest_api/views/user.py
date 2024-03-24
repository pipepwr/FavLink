from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate, login, logout


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
                    {"message": error_messages},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user = User.objects.create_user(
                username=user_name, email=email, password=password
            )
            user.save()
            return Response(
                {"message": "Create user Complete", "data": user_serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"message": user_serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


class LoginView(APIView):
    """
    Login
    """

    def post(self, request):

        user_name = request.data.get("username")
        password = request.data.get("password")

        if user_name and password:
            user = authenticate(request, username=user_name, password=password)
            if user is not None:
                login(request, user)
                return Response(
                    {"message": "Login Complete"}, status=status.HTTP_202_ACCEPTED
                )
            else:
                return Response(
                    {"message": "Cant Login With these user and Password"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )


class LogoutView(APIView):
    """
    Logout
    """

    def post(self, request):
        if request.user.is_authenticated:
            logout(request)
            return Response(
                {"message": "Log out Complete"},
                status=status.HTTP_202_ACCEPTED,
            )
        else:
            return Response(
                {"message": "Please Log in"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
