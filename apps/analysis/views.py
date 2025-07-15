from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.management import call_command
from .utils import get_collection
from .utils import CROSS_DATA_COLLECTION, LONG_DATA_COLLECTION, MERGED_DATA, RF_RESULT, Y_RESULT


class RFResultView(APIView):
    permission_classes = [IsAuthenticated]
    async def get(self, request):
        doc = get_collection(RF_RESULT).find_one({'_id':'latest'}) or {}
        return Response(doc.get('report', {}), content_type="application/json")

class YProbView(APIView):
    permission_classes = [IsAuthenticated]
    async def get(self, request):
        doc = get_collection(Y_RESULT).find_one({'_id':'latest'}) or {}
        return Response(doc.get('y_prob', {}), content_type="application/json")

class DataView(APIView):
    permission_classes = [IsAuthenticated]
    async def get(self, request):
        data = list(get_collection(MERGED_DATA).find({}))
        for d in data: d.pop('_id', None)
        return Response(data, content_type="application/json")

class TrainModelView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            call_command('train_model')
        except Exception as e:
            return Response({"detail": str(e)}, status=500)
        return Response({"detail": "Training started"}, status=200)
