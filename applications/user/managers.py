from django.db import models
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
	def create_user(self, email, password = None, **extra_fields):
		if not email:
			raise ValueError("Debe ingresar un email")
		if password is None:
			raise ValueError("Debe ingresar una contraseña")
		
		user = self.model(
			email = self.normalize_email(email),
			**extra_fields
		)

		user.set_password(password)
		user.save(using = self._db)
		return user

	def create_superuser(self, email, password = None, **extra_fields):
		user = self.create_user(email, password, **extra_fields)
		user.is_admin = True
		user.is_staff = True
		user.is_superadmin = True

		user.save(using = self._db)
		return user