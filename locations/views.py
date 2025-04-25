from rest_framework.viewsets import ViewSet
from .models import Branch
from .serializers import BranchSerializer
from rest_framework.response import Response

class BranchViewSet(ViewSet):

    def list(self, request, *args, **kwargs):
        queryset = Branch.objects.all()
        serializer = BranchSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    