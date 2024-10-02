from classes.managers import ExcludeDeletedObjectsManager
from django.contrib.auth.models import UserManager

class UserManager(UserManager, ExcludeDeletedObjectsManager):
    def does_user_exist(self, query):
        return super().get_queryset().filter(**query).exists()
    
    # overrode username as required field for creating user
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email must be set')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    # overrode username as required for creating superuser.
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)