from rest_framework.response import Response
from users.models import User

class CheckPerformTransaction:
    def __call__(self, params):
        data = params.get("params", {})
        account = data.get("account", {})
        amount = data.get("amount")

        # 1. Foydalanuvchini topish
        user_id = account.get("login")
        if not user_id:
            return self._error(-31050, "User ID yo'q")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return self._error(-31050, "Foydalanuvchi topilmadi")

        # 2. To‘lov qabul qilishga ruxsat bormi?
        if not user.is_active:
            return self._error(-31051, "Foydalanuvchi tasdiqlanmagan yoki faol emas")

        # 3. Summani tekshirish (masalan: minimal yoki maksimal)
        if amount < 1000:  # so'm (Payme 1 so‘m = 100 in API)
            return self._error(-31001, "Minimal summa 1000 som bolishi kerak")

        # 4. Hammasi yaxshi bo‘lsa:
        return Response({
            "result": {
                "allow": True
            }
        })

    def _error(self, code, message):
        return Response({
            "error": {
                "code": code,
                "message": {
                    "uz": message,
                    "ru": message,
                    "en": message
                },
                "data": None
            }
        })


