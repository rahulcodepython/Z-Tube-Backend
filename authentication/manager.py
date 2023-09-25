from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager): 

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")

        user = self.model(
            email=self.normalize_email(email).lower(),
            **extra_fields
        )

        user.set_password(password) 
        user.save(using=self._db) 
        return user

    def create_superuser(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        if not password:
            raise ValueError('Password is not provided')

        user = self.model(
            email=self.normalize_email(email).lower(),
            is_superuser=True,
            **extra_fields
        )

        user.set_password(password) 
        user.save(using=self._db) 
        return user