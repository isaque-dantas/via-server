from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.services.report import ReportService


class ReportViewSet(APIView):
    @staticmethod
    def get(request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        reports = ReportService.get_reports()

        return Response(reports, status=status.HTTP_200_OK)
