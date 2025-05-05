from rest_framework import status
from rest_framework.parsers import BaseParser
from rest_framework.response import Response
from rest_framework.views import APIView

from api.services.vowel_reader import VowelReaderService


class PlainTextParser(BaseParser):
    media_type = 'text/plain'

    def parse(self, stream, media_type=None, parser_context=None):
        return stream.read()


class VowelReaderViewSet(APIView):
    parsel_classes = [PlainTextParser]

    def post(self, request):
        print(request.data)
        if not request.data.get('string'):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        vowel_reading_data = VowelReaderService.get_reading_data(request.data.get('string'))

        return Response(vowel_reading_data, status=status.HTTP_200_OK)
