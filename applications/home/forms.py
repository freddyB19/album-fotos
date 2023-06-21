from django import forms 

from . import models

class CategoryForm(forms.ModelForm):
	
	class Meta:
		model = models.Category
		fields = (
			'name',
			'active'
		)

		widgets = {
			'name': forms.TextInput(
				attrs = {
					'class': 'form-control rounded-4'
				}
			),
			'active': forms.CheckboxInput(
				attrs = {
					'class': 'form-check-input'
				}
			),
		}

	def clean_name(self):
		name = self.cleaned_data["name"]
		if len(name) < 2:
			self.add_error('name', 'El nombre resulta ser muy corto.')
		return name 


class CategoryUpdateNameForm(forms.Form):
	name = forms.CharField(label = "Nombre", required = True, widget=forms.TextInput(attrs={"class": 'form-control rounded-4'}))


	def __init__(self, user = None, *args, **kwargs):
	    super().__init__(*args, **kwargs)
	    self.user_pk = user



	def clean(self):
		self.cleaned_data = super().clean()
		name = self.cleaned_data.get('name', None)


		if models.Category.objects.filter(user_category = self.user_pk, name = name).exists():
			#raise forms.ValidationError("Ya existe una categoria con ese nombre.")
			self.add_error('name', 'Ya existe una categoria con ese nombre.')
		return name





class SaveImageForm(forms.ModelForm):
	all_category = forms.ModelChoiceField(
		label = 'Categorias',
		queryset = None,
		required = True,
		widget = forms.Select(
			attrs = {
				'class': 'form-select'
			}
		)
	)

	class Meta:
		model = models.Image
		fields = (
			'photo',
			'title',
			'description',
		)

		widgets = {
			'title': forms.TextInput(
				attrs = {
					"class": 'form-control rounded-4'
				}
			),
			'description': forms.Textarea(
				attrs = {
					"class": 'form-control'
				}
			),
			'photo': forms.FileInput(
				attrs = {
					"class": 'form-control rounded-4'
				}
			)

		}

	def __init__(self, user, *args, **kwargs):
	    super().__init__(*args, **kwargs)
	    self.fields['all_category'].queryset = models.Category.objects.filter(
	    	user_category_id = user, 
			active = True
	    )





class ImageDetailForm(forms.ModelForm):

	class Meta:
		model = models.Image
		fields = (
			'title',
			'description',
		)

		widgets = {
			'title': forms.TextInput(
				attrs = {
					"class": 'form-control rounded-4'
				}
			),
			'description': forms.Textarea(
				attrs = {
					"class": 'form-control'
				}
			),
		}