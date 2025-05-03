from users.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

class UserStatsAPIView(ViewSet):
    permission_classes = [IsAdminUser]  # faqat admin foydalanuvchi uchun

    def get(self, request):
        user_count = User.objects.count()
        return Response({
            "total_users": user_count,
            "active_users": User.objects.filter(is_verified=True).count(),
        })
