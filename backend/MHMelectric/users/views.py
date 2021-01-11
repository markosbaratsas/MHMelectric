from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from users.models import API_key
from users.serializers import RegistrationSerializer


@api_view(['POST', ])
def register_user(request):
    
    if request.method == "POST":
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = 'Successfully created a new user.'
            data['email'] = user.email
            data['username'] = user.username
            data['token'] = Token.objects.get(user=user).key
        else: 
            data = serializer.errors
        return Response(data)

@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def delete_token(request):

    if request.method == "POST":
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass

        return Response(status=status.HTTP_200_OK)

@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def admin_create_user(request, username, password):

    # check if user is superuser
    if request.user.is_superuser:
        # if user exists get User object, else create it
        user, created = User.objects.get_or_create(username=username)
        user.set_password(password)
        user.save()

        if created:
            return Response({'Success': f'User {username} created'}, status=status.HTTP_200_OK)
        else:
            return Response({'Success': f'Password updated for {username}'}, status=status.HTTP_200_OK)

    else:
        return Response({'Failed': 'Not authorized'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def admin_get_user(request, username):

    # check if user is superuser
    if request.user.is_superuser:
        # if user exists get User object, else create it
        try:
            user = User.objects.get(username=username)

            data = {}
            data['username'] = user.username
            data['email'] = user.email
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response({'No data'}, status=status.HTTP_402_PAYMENT_REQUIRED)

    else:
        return Response({'Failed': 'Not authorized'}, status=status.HTTP_401_UNAUTHORIZED)

# inherit class ObtainAuthToken () https://github.com/encode/django-rest-framework/blob/master/rest_framework/authtoken/views.py )
# and change just the post method
class ObtainAPIKey(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)

        api_key = token.key[0:4] + "-" + token.key[4:8] + "-" + token.key[8:12]
        API_key.objects.get_or_create(api_key=api_key, token=token)

        return Response({'api_key': api_key}, status=status.HTTP_200_OK)

@api_view(['POST', ])
def cli_logout(request):

    if request.method == "POST":
        try:
            api_key = API_key.objects.get(api_key=request.data['api_key'])
            api_key.token.delete() # delete token and API_key object will be automatically deleted
        except (AttributeError, ObjectDoesNotExist):
            pass

        return Response(status=status.HTTP_200_OK)

@api_view(['GET', ])
def get_token_from_api_key(request):

    if request.method == "GET":
        try:
            api_key = API_key.objects.get(api_key=request.data['api_key'])
            return Response({'token': api_key.token.key}, status=status.HTTP_200_OK)
        except (AttributeError, ObjectDoesNotExist):
            return Response({'Failed': 'API key not found'}, status=status.HTTP_200_OK)
