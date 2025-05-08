from django.db.models import Manager


class CartManager(Manager):
    
    def get_or_create_cart(self, user=None, session_id=None):
        if user and user.is_authenticated:
            cart, created = self.get_or_create(user=user)
        elif session_id:
            cart, created = self.get_or_create(session_id=session_id)
        else:
            cart, created = None, False
        return cart
