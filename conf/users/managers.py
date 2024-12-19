from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _
import re

class CustomUserManager(BaseUserManager):
    def create_user(self, phone, username, email=None, password=None, **extra_fields):
        if not phone:
            raise ValueError(_('The Phone number must be set'))
        if not username:
            raise ValueError(_('The Username must be set'))

        phone = self.normalize_phone(phone)
        user = self.model(phone=phone, username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(phone, username, email, password, **extra_fields)

    def normalize_phone(self, phone):
        normalized_phone = re.sub(r'[ ()-]', '', phone)
        
        phone_regex = r"^(0|98)?([ ]|-|[()]){0,2}9[0-4|9]([ ]|-|[()]){0,2}(?:[0-9]([ ]|-|[()]){0,2}){8}$"
        if not re.match(phone_regex, normalized_phone):
            raise ValueError(_('The phone number is not valid'))
        
        return normalized_phone