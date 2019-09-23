from rest_framework import viewsets
from .serializers import HoldingSerializer
from .models import Holding
from rest_framework.response import Response


class HoldingViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving holdings.
    """
    def list(self, request):
        queryset = Holding.objects.all()
        serializer = HoldingSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Holding.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = HoldingSerializer(user)
        return Response(serializer.data)
