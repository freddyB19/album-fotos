from django.shortcuts import render
from django.views import generic
from django.views.generic import detail
from django.views.generic import edit
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect

from . import forms, models
from applications.functions import new_name_image



# Create your views here.

class IndexView(generic.TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_images'] = models.Image.objects.filter(
        	author_id = self.request.user.pk 
        )[:5]
        # Solo debe devolver las 5 primeras fotos
        
        if not len(context['list_images']):
        	
        	context['list_images_home_page'] = models.ImagesHomePage.objects.all()
        

        context['last_images'] = models.Image.objects.filter(
        	author_id = self.request.user.pk 
        ).order_by('-id')[:10]

        context['categorys_deactive'] = models.Category.objects.filter(
        	user_category_id = self.request.user.pk,
        	active = False
        )
        return context


class NewCategoryFormView(LoginRequiredMixin, generic.FormView):
	form_class = forms.CategoryForm
	model = models.Category
	template_name = "home/add_category.html"
	success_url = reverse_lazy('home:index')
	login_url = reverse_lazy('user:login')


	def form_valid(self, form):
		if form.is_valid():
			category = models.Category(
				name = form.cleaned_data["name"],
				active = form.cleaned_data["active"],
				user_category_id = self.kwargs.get('pk')
			)
			category.url = category.get_slug()
			category.save()

			messages.add_message(self.request, messages.INFO, 'Categoria creada de manera exitosa.')

		return super().form_valid(form)



class AllCategoryListView(LoginRequiredMixin, generic.ListView):
	template_name = "home/list_category.html"
	context_object_name = 'categorys'
	login_url = reverse_lazy('user:login')


	def get_queryset(self):
		return models.Category.objects.filter(
			user_category_id = self.request.user.pk, 
			active = True
		)



class CategoryDetailView(LoginRequiredMixin, generic.ListView):
    model = models.Category
    context_object_name = 'categorys'
    template_name = "home/detail_category.html"
    paginate_by = 5
    login_url = reverse_lazy('user:login')

    
    def get_queryset(self):
    	return models.Image.objects.filter(
        	image_category = self.kwargs.get('pk'),
        	author_id = self.request.user.pk
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['category_detail'] = models.Category.objects.get(pk = self.kwargs.get('pk')) 
        
        context['total_photo'] = models.Image.objects.filter(
        	image_category = self.kwargs.get('pk'),
        	author_id = self.request.user.pk
        ).count()
        return context




class CategoryNameUpdate(LoginRequiredMixin, edit.FormView):
	form_class = forms.CategoryUpdateNameForm
	template_name = "home/update_category.html"
	login_url = reverse_lazy('user:login')
	success_url = reverse_lazy('home:list-categorys')
	
	def get_context_data(self, **kwargs):
	    context = super().get_context_data(**kwargs)
	    
	    context['name'] = models.Category.objects.get(
        	user_category = self.request.user.pk,
        	pk = self.kwargs.get('pk')
        ).name

	    return context


	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs.update({
			'user': self.request.user.pk
		})
		return kwargs

	
	def form_valid(self, form):
		if form.is_valid():
			update_name = models.Category.objects.get(
				pk = self.kwargs.get('pk'),
				user_category = self.request.user.pk
			)

			update_name.name = form.cleaned_data
			update_name.save()

			messages.add_message(self.request, messages.INFO, 'Nombre de la categoria actualizado.')


		return super().form_valid(form)


class CategoryDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = models.Category
    template_name = "home/delete_category.html"
    success_url = reverse_lazy('home:index')
    login_url = reverse_lazy('user:login')


    def get(self, request, *args, **kwargs):
    	messages.add_message(self.request, messages.INFO, 'La categoria fue eliminada correctamente')
    	return super().get(request, *args, **kwargs)
    



class CategoryStatusUpdateView(LoginRequiredMixin, edit.UpdateView):
	login_url = reverse_lazy('user:login')

	def post(self, request, *args, **kwargs):
		print(kwargs)
		
		try:
			category = get_object_or_404(models.Category, pk=kwargs['pk'])
			data = 'La categoria se encuentra en modo'
			
			if category.active:
				category.active = False
				data = f"{data} oculto"
			else:
				category.active = True
				data = f"{data} visible"
						
			messages.add_message(self.request, messages.INFO, data)
		
			category.save()
		except models.Category.DoesNotExist as e:
			messages.add_message(self.request, messages.ERROR, 'No existe registro de esta categoría')
			
		
		return HttpResponseRedirect(
			reverse(
				'user:settings-user', 
				kwargs = {
					'pk': self.request.user.pk
				}
			)		
		)



class SaveImageView(LoginRequiredMixin, edit.FormView):
	form_class = forms.SaveImageForm
	template_name = "home/add_image.html"
	success_url = reverse_lazy('home:index')
	login_url = reverse_lazy('user:login')


	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs.update({
			'user': self.request.user.pk
		})
		return kwargs


	async def form_valid(self, form):
		if form.is_valid():
			new_photo = models.Image(
				title = form.cleaned_data['title'],
				description = form.cleaned_data['description'],
				image_category = form.cleaned_data['all_category'],
				author = self.request.user,
			)
			file_new_name = new_name_image(form.cleaned_data["photo"])
			
			new_photo.photo = file_new_name
			new_photo.save()

			messages.add_message(self.request, messages.INFO, 'Nueva foto agregada.')

		return super().form_valid(form)



class ImageDetailView(LoginRequiredMixin, generic.DetailView):
	template_name = 'home/detail_image.html'
	model = models.Image
	login_url = reverse_lazy('user:login')


	def get_context_data(self, **kwargs):
	    context = super().get_context_data(**kwargs)
	    
	    image = models.Image.objects.get(pk = self.kwargs.get('pk'))
	    context['form_detail'] = forms.ImageDetailForm(initial={
	    	'title': image.title,
	    	"description" : image.description
	    })
	    
	    return context


class UpdateImageView(LoginRequiredMixin, edit.UpdateView):
	login_url = reverse_lazy('user:login')

	def post(self, request, *args, **kwargs):
		
		update_photo = models.Image.objects.get(
			pk = kwargs.get('pk')
		)

		update_photo.title = request.POST.get('title', update_photo.title)
		update_photo.description = request.POST.get('description', update_photo.description)
		update_photo.save()

		messages.add_message(self.request, messages.INFO, 'Datos de la foto actualizados.')
		
		return HttpResponseRedirect(
			reverse('home:detail-photo', kwargs = {'pk': kwargs.get('pk')})
		)



class ImageDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = models.Image
    template_name = "home/delete_image.html"
    success_url = reverse_lazy('home:index')
    login_url = reverse_lazy('user:login')


    def get(self, request, *args, **kwargs):
    	messages.add_message(self.request, messages.INFO, 'La foto fue eliminada correctamente')
    	return super().get(request, *args, **kwargs)




class Error404TemplateView(generic.TemplateView):
	template_name = 'home/error_404.html'