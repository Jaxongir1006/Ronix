from rest_framework.viewsets import ViewSet
from .models import Branch
from .serializers import BranchSerializer
from rest_framework.response import Response
from django.core.cache import cache
class BranchViewSet(ViewSet):

    def list(self, request, *args, **kwargs):
        cache_key = 'branches_list'
        data = cache.get(cache_key)
        if data:
            return Response(data, status=200)
        queryset = Branch.objects.all()
        serializer = BranchSerializer(queryset, many=True, context={'request': request})

        cache.set(cache_key, serializer.data, timeout=60*60)

        return Response(serializer.data)
    