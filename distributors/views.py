from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Distributor
from .serializer import DistributorSerializer

# class DistributorViewSet(viewsets.ModelViewSet):
#     queryset = Distributor.objects.all()
#     serializer_class = DistributorSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

#     def perform_create(self, serializer):
#         serializer.save(created_by=self.request.user)

class DistributorViewSet(viewsets.ModelViewSet):
    queryset = Distributor.active.all()
    serializer_class = DistributorSerializer