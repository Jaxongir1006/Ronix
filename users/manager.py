from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def distributors(self):
        return self.filter(is_distributor=True)

    def with_email(self):
        return self.exclude(email__isnull=True).exclude(email__exact="")