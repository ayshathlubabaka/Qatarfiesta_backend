from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, name, email=None, password=None):
        if not email:
            raise ValueError("User must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_organizer(self, name, email, password=None, **extra_fields):
        user = self.create_user(name, email, password=password, **extra_fields)
        user.is_organizer = True
        user.save()
        return user

    def create_superuser(self, name, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            name=name,
        )

        user.is_active = True
        user.is_registered = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
