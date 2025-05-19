from users.models import User

def check_perform_transaction(amount, account):
    user_id = account.get("login")
    if not user_id:
        return {"success": False, "error": {
            "code": -31050,
            "message": {
                "uz": "Foydalanuvchi identifikatori yo'q",
                "ru": "He найден идентификатор пользователя",
                "en": "User ID is missing"
            }
        }}

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return {"success": False, "error": {
            "code": -31050,
            "message": {
                "uz": "Foydalanuvchi topilmadi",
                "ru": "Пользователь не найден",
                "en": "User not found"
            }
        }}

    if not user.is_active or not user.is_verified:
        return {"success": False, "error": {
            "code": -31051,
            "message": {
                "uz": "Foydalanuvchi faol emas yoki tasdiqlanmagan",
                "ru": "Пользователь неактивен или не подтвержден",
                "en": "User inactive or not verified"
            }
        }}

    if not isinstance(amount, int) or amount < 100000:  # 1000 so‘m = 100000 tiyin
        return {"success": False, "error": {
            "code": -31001,
            "message": {
                "uz": "Minimal summa 1000 som bolishi kerak",
                "ru": "Минимальная сумма — 1000 сум",
                "en": "Minimum amount must be 1000 UZS"
            }
        }}

    return {"success": True}
