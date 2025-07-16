from adrf.views import APIView
from django.core.management import call_command
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.common.repositories.analysis_repository import (
    MergedDataRepository,
    RFResultRepository,
    YProbRepository,
)


class RFResultView(APIView):
    """Return the latest random forest metrics."""

    permission_classes = [IsAuthenticated]

    async def get(self, request):
        result = await RFResultRepository().latest()
        return Response(result, content_type="application/json")


class YProbView(APIView):
    """Return probability predictions from the last run."""

    permission_classes = [IsAuthenticated]

    async def get(self, request):
        result = await YProbRepository().latest()
        return Response(result, content_type="application/json")


class DataView(APIView):
    """Return the merged dataset used for training."""

    permission_classes = [IsAuthenticated]

    async def get(self, request):
        result = await MergedDataRepository().all()
        return Response(result, content_type="application/json")


class TrainModelView(APIView):
    """Trigger the ML training pipeline."""

    permission_classes = [IsAuthenticated]

    async def post(self, request):
        call_command("train_model")
        return Response({"detail": "Training started"})
