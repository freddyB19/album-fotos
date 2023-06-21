import os

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect

from django.views import generic
from django.views.generic import edit

from django.db import models as db_models
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


from applications.functions import new_name_image
from applications.home.models import Category

from . import models, forms



# Create your views here.

class SettingsUserTemplateView(LoginRequiredMixin, generic.TemplateView):
	template_name = "user/settings.html"
	login_url = reverse_lazy('user:login')

	
	def get_context_data(self, **kwargs):
	    context = super().get_context_data(**kwargs)
	    context['total_categorys'] =  self.request.user.categorylist.count()
	    context['categorias_user'] = self.request.user.categorylist.all()[:3]
	    context['photo_user'] =  self.request.user.imagelist.count()
	    context['form_photo'] = forms.UpdatePhotoUserForm
	    context['categorys_deactive'] = Category.objects.filter(user_category_id = self.request.user.id, active = False)
	    return context


class CreateUserFormView(generic.FormView):
	form_class = forms.CreateUserForm
	model = models.User
	template_name = "user/create_user.html"
	success_url = reverse_lazy("user:login")

	async def form_valid(self, form):
		if form.is_valid():
			if form.cleaned_data["photo"]:
				photo = new_name_image(form.cleaned_data["photo"])
			else:
				photo = form.cleaned_data["photo"]

			user = models.User.objects.create_user(
				form.cleaned_data["email"],
				form.cleaned_data["password_1"],
				first_name = form.cleaned_data["first_name"],
				last_name = form.cleaned_data["last_name"],
				photo = photo
			)
			messages.add_message(self.request, messages.INFO, 'Usuario creado de manera exitosa.')
		return super().form_valid(form)



class LoginUserFormView(edit.FormView):
	form_class = forms.LoginUserForm
	template_name = "user/login.html"
	success_url = reverse_lazy("home:index")

	def get(self, request, *args, **kwargs):
		if self.request.user.is_authenticated:
			return HttpResponseRedirect(
				reverse(
					'home:index'
				)
			)
		return super().get( request, *args, **kwargs)

	def form_valid(self, form):
		if form.is_valid():
			user = authenticate(
				email = form.cleaned_data["email"], 
				password = form.cleaned_data["password"]
			)
			login(self.request, user)
		return super().form_valid(form)



class LogoutUserView(LoginRequiredMixin, generic.View):
	login_url = reverse_lazy('user:login')

	def get(self, request, *args, **kwargs):
		logout(request)
		return HttpResponseRedirect(
			reverse(
				'home:index'
			)
		)



class UpdatePasswordUser(LoginRequiredMixin, generic.FormView):
	form_class = forms.NewPasswordUserForm
	template_name = 'user/update_password.html'
	login_url = reverse_lazy('user:login')



	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs.update({
			'user_email': self.request.user.email
		})
		return kwargs

	def form_valid(self, form):
		if form.is_valid():

			messages.add_message(self.request, messages.INFO, 'La contraseña fue cambiada de manera exitosa.')
			
			try:
				user = get_object_or_404(models.User, pk = self.kwargs.get('pk'))
				
				new_password = form.cleaned_data['password_new_1']	
				user.set_password(new_password)
				user.save()
				
			except models.User.DoesNotExist as e:
				messages.add_message(self.request, messages.ERROR, 'Ha ocurrido un error durante el proceso, vuelve a intentarlo.')
			
			logout(self.request)
		return HttpResponseRedirect(
				reverse(
					'user:login', 
				)
			)


class UpdateUserEmailFormView(LoginRequiredMixin, edit.FormView):
	form_class = forms.UpdateUserEmailForm
	template_name = "user/update_email.html"
	login_url = reverse_lazy('user:login')


	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs.update({
			'email': self.request.user.email
		})
		return kwargs


	def form_valid(self, form):
		if form.is_valid():
			new_email = form.cleaned_data['email']

			data = f'Los cambios (Nuevo email: {new_email}) se realizaron correctamente.'
			messages.add_message(self.request, messages.INFO, data)
			
			try:
				user = get_object_or_404(models.User, pk = self.kwargs.get('pk'))
				
				user.email = new_email
				user.save()
				
			except models.User.DoesNotExist as e:
				messages.add_message(self.request, messages.ERROR, 'Ha ocurrido un error durante el proceso, vuelve a intentarlo.')

		return HttpResponseRedirect(
				reverse(
					'user:settings-user', 
					kwargs = {
						'pk': self.request.user.pk
					}
				)
			)




class UpdatePhotoUserView(LoginRequiredMixin, generic.View):
	login_url = reverse_lazy('user:login')

	
	def post(self, request, *args, **kwargs):
		new_photo = request.FILES.get('photo', None)

		if new_photo:
			messages.add_message(self.request, messages.INFO, 'Foto de perfil actualizada correctamente')
			try:
				user = get_object_or_404(models.User, pk = kwargs.get('pk'))
				new_photo = new_name_image(new_photo)

				new_photo.name = os.path.join(user.get_path_image(), new_photo.name)
				user.photo = new_photo

				user.save()
			except models.User.DoesNotExist as e:
				messages.add_message(self.request, messages.ERROR, 'Ha ocurrido un error durante el proceso, vuelve a intentarlo.')
 
		return HttpResponseRedirect(
			reverse(
				'user:settings-user',
				kwargs = {
					'pk': self.request.user.pk
				}
			)
		)

