from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.management import call_command
from django.forms.models import model_to_dict
from apps.common.repositories.analysis_repository import (
    RFResultRepository,
    YProbRepository,
    MergedDataRepository,
)


class RFResultView(APIView):
    permission_classes = [IsAuthenticated]

    async def get(self, request):
        repo = RFResultRepository()
        result = repo.latest()
        report = result.report if result else {}
        return Response(report, content_type="application/json")

class YProbView(APIView):
    permission_classes = [IsAuthenticated]

    async def get(self, request):
        repo = YProbRepository()
        result = repo.latest()
        y_prob = result.y_prob if result else {}
        return Response(y_prob, content_type="application/json")

class DataView(APIView):
    permission_classes = [IsAuthenticated]

    async def get(self, request):
        repo = MergedDataRepository()
        records = [model_to_dict(obj) for obj in repo.get_all()]
        return Response(records, content_type="application/json")

class TrainModelView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            call_command('train_model')
        except Exception as e:
            return Response({"detail": str(e)}, status=500)
        return Response({"detail": "Training started"}, status=200)
