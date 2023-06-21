import os 

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from . import managers

class User(AbstractBaseUser, PermissionsMixin):

	first_name = models.CharField(max_length = 20, blank=True, null=True)
	last_name = models.CharField(max_length = 20, blank=True, null=True)
	email = models.EmailField(unique=True)
	photo = models.ImageField(blank=True, null = True, upload_to="uploads/perfil/")

	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default = False)
	is_admin = models.BooleanField(default=False)
	is_superadmin = models.BooleanField(default=False)



	objects = managers.UserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS =  ['first_name', 'last_name']

	class Meta:
		verbose_name = 'Usuario'
		verbose_name_plural = 'Usuarios'

	def get_full_name(self):
		return f"{self.first_name} {self.last_name}"

	def get_username(self):
		username, host = self.email.split('@')
		return f'@{username}'



	# Si tiene permisos de admin
	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, add_label):
		return True

	def __str__(self):
		return f"{self.email}"

