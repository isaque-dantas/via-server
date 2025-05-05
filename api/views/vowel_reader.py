from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.services.vowel_reader import VowelReaderService


class VowelReaderViewSet(APIView):
    @staticmethod
    def post(request):
        vowel_reading_data = VowelReaderService.get_reading_data(request.data)

        return Response(vowel_reading_data, status=status.HTTP_200_OK)
