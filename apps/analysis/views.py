from asgiref.sync import sync_to_async
from adrf.views import APIView
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
        result = await RFResultRepository().latest()
        return Response(result, content_type="application/json")

class YProbView(APIView):
    permission_classes = [IsAuthenticated]

    async def get(self, request):
        result = await YProbRepository().latest()
        return Response(result, content_type="application/json")

class DataView(APIView):
    permission_classes = [IsAuthenticated]

    async def get(self, request):
        result = await MergedDataRepository().all()
        return Response(result, content_type="application/json")

class TrainModelView(APIView):
    permission_classes = [IsAuthenticated]
    async def post(self, request):
        try:
            await sync_to_async(call_command('train_model'))
        except Exception as e:
            return Response({"detail": str(e)}, status=500)
        return Response({"detail": "Training started"}, status=200)
