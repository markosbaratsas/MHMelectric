from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

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
