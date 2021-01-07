from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FileUploadParser

from rest_api.models import Car, UploadedCSV
from rest_api.serializers import CarSerializer, UploadedCSVSerializer
from rest_api.scripts import upload_csv_file

def index(request):
    return HttpResponse("<h1>We made it so far!</h1>")

# we could do something like this for the other requests
@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def get_first_car(request):
    try:
        cars = Car.objects.all()
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    car = list(cars)[0]
    if request.method == "GET":
        serializer = CarSerializer(car)
        return Response(serializer.data)


@permission_classes((IsAuthenticated,))
class SessionsUpload(APIView):
    parser_classes = (MultiPartParser, FileUploadParser,)
    serializer = UploadedCSVSerializer

    def post(self, request, format='csv'):
        if request.user.is_superuser:
            upload = self.serializer(data=request.FILES)
            if upload.is_valid() and self.serializer.check_extension(request.FILES['file'].name):
                file = UploadedCSV.objects.create(csv_file=upload.validated_data['file'], uploaded_from=request.user)

                data = upload_csv_file(file)
                return Response(data, status.HTTP_200_OK)
            else:
                data = upload.errors
                return Response(data, status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'Failed': 'Not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
