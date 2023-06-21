from django import forms
from django.contrib.auth import authenticate

from . import models


class CreateUserForm(forms.ModelForm):
	password_1 = forms.CharField(
		label = 'Contraseña',
		required = True,
		widget = forms.PasswordInput(
			attrs = {
				"placeholder": "Contraseña",
				"class": 'form-control rounded-4'
			}
		)
	)
	password_2 = forms.CharField(
		label = 'Contraseña (confirmar)',
		required = True,
		widget = forms.PasswordInput(
			attrs = {
				"placeholder": "Repetir Contraseña",
				"class": 'form-control rounded-4'
			}
		)
	)


	class Meta:
		model = models.User
		fields = (
			"first_name",
			"last_name",
			"email",
			"photo",
		)

		widgets = {
			'first_name': forms.TextInput(
				attrs = {
					"class": 'form-control rounded-4'
				}
			),
			'last_name': forms.TextInput(
				attrs = {
					"class": 'form-control rounded-4'
				}
			),
			'email': forms.EmailInput(
				attrs = {
					"class": 'form-control rounded-4'
				}
			),
			'photo': forms.FileInput(
				attrs = {
					"class": 'form-control rounded-4'
				}
			)

		}


	def clean_password_1(self):
		password_1 = self.cleaned_data["password_1"]

		if len(password_1) < 5:
			self.add_error("password_1", "La contraseña es muy corta")

		return password_1

	def clean_password_2(self):
		password_1 = self.cleaned_data["password_1"]
		password_2 = self.cleaned_data["password_2"]

		if password_1 != password_2:
			self.add_error("password_2", "Las contraseñas no son identicas.")

		return password_2


	def clean_email(self):
		email = self.cleaned_data["email"]

		if models.User.objects.filter(email = email).exists():
			self.add_error("email", "Ya existe un registro con un mismo email.")


		return email




class LoginUserForm(forms.Form):
	email = forms.EmailField( 
		required = True,
		widget = forms.EmailInput(
			attrs = {
				"class": 'form-control rounded-4'
			}
		)
	)
	password = forms.CharField(
		label = "Contraseña",
		required = True,
		widget = forms.PasswordInput(
			attrs = {
				"class": 'form-control rounded-4'
			}
		)
	)

	def clean(self):
		self.cleaned_data = super().clean()
		email = self.cleaned_data["email"]
		password = self.cleaned_data["password"]

		if not authenticate(email = email, password = password):
			raise forms.ValidationError("Datos de certificación del usuario invalidos")

		return self.cleaned_data



class UpdateUserEmailForm(forms.Form):
	email = forms.EmailField(
		label = 'Nuevo Email',
		required = True,
		widget = forms.EmailInput(
			attrs = {
				'placeholder': 'Ingrese un nuevo email valido',
				"class": 'form-control rounded-4'
			}
		)
	)

	password_conf = forms.CharField(
		label = 'Contraseña',
		help_text = 'Ingrese su contraseña para confirmar.',
		required = True,
		widget = forms.PasswordInput(
			attrs = {
				'placeholder': 'Ingrese su contraseña para confirmar.',
				"class": 'form-control rounded-4'
			}
		)
	)

	def __init__(self, email,*args, **kwargs):
	    super().__init__(*args, **kwargs)
	    self.email_user = email

	def clean_email(self):
		email = self.cleaned_data['email']

		if models.User.objects.filter(email = email).exists():
			self.add_error('email', 'Ya existe el registro de un usuario con ese email.')

		return email

	def clean_password(self):
		password = self.cleaned_data['password_conf']

		if len(password) < 5:
			self.add_error("password_conf", "La contraseña es muy corta")
		return password


	def clean(self):
		self.cleaned_data = super().clean()

		password = self.cleaned_data['password_conf']

		if not authenticate(email = self.email_user, password = password):
			raise forms.ValidationError("Datos de certificación del usuario invalidos")

		return self.cleaned_data



class UpdatePhotoUserForm(forms.ModelForm):
	class Meta:
		model = models.User
		fields = ('photo',)
	
		widgets = {
			'photo': forms.FileInput(
				attrs = {
					"class": 'form-control rounded-4'
				}
			)
		}

	def clean_photo(self):
		photo = self.cleaned_data['photo']

		if not photo:
			self.add_error('photo', 'Debe ingresar una nueva foto.')

		return photo


class NewPasswordUserForm(forms.Form):
	password_new_1 = forms.CharField(
		label = 'Nueva Contraseña',
		required = True,
		widget = forms.PasswordInput(
			attrs = {
				"placeholder": "Contraseña",
				"class": 'form-control rounded-4'
			}
		)

	)
	password_new_2 = forms.CharField(
		label = 'Repita la nueva contraseña',
		required = True,
		help_text = 'Ingrese su contraseña actual para confirmar los cambios.',
		widget = forms.PasswordInput(
			attrs = {
				"placeholder": "Repetir Contraseña",
				"class": 'form-control rounded-4'
			}
		)

	)
	password_act = forms.CharField(
		label = 'Contraseña actual',
		required = True,
		widget = forms.PasswordInput(
			attrs = {
				"placeholder": "Confirmación (contraseña)",
				"class": 'form-control rounded-4'
			}
		)

	)


	def __init__(self, user_email, *args, **kwargs):
	    super().__init__(*args, **kwargs)
	    self.user_email =  user_email

	def clean_password_act(self):
		password_act = self.cleaned_data['password_act']

		if not authenticate(email = self.user_email, password = password_act):
			raise forms.ValidationError('La Contraseña actual no coincide con el usuario.')

		return password_act

	def clean_password_new_1(self):
		password_new_1 = self.cleaned_data['password_new_1']

		if len(password_new_1) < 5:
			self.add_error('password_new_1', 'La contraseña ingresada es muy corta.')

		return password_new_1

	def clean(self):
		self.cleaned_data = super().clean()
		
		password_new_1 = self.cleaned_data['password_new_1']
		password_new_2 = self.cleaned_data['password_new_2']

		if password_new_1 != password_new_2:
			self.add_error('password_new_2', 'Las contraseñas no coinciden.')

		return self.cleaned_data
