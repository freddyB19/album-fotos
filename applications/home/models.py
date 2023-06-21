from django.db import models

from applications.user.models import User


class Category(models.Model):
	name = models.CharField(max_length=30)
	created = models.DateField(auto_now_add=True)
	updated = models.DateField(auto_now=True)
	active = models.BooleanField(default=True)
	url = models.SlugField(max_length=20, blank=True, null=True)
	user_category = models.ForeignKey(
		User,
		related_name = 'categorylist',
		on_delete = models.CASCADE,
		blank=True,
		null=True
	)

	class Meta:
		verbose_name = "Category"
		verbose_name_plural = "Categorys"

	def __str__(self):
		return f'{self.name}'
	
	def get_slug(self):
		return self.name.strip().lower().replace(" ", "-")
    


class Image(models.Model):
	photo = models.ImageField(upload_to="uploads/gallery/", blank=True, null = True)
	
	created = models.DateField(auto_now_add=True)
	title = models.CharField(max_length=30, default = "IMAGE")
	description = models.TextField(blank=True, null=True)
	author = models.ForeignKey(
		User,
		on_delete = models.CASCADE,
		related_name = 'imagelist'
	)
	image_category = models.ForeignKey(
		Category,
		on_delete = models.CASCADE,
		related_name = 'image_category_list'
	)

	class Meta:
		verbose_name = "Image"
		verbose_name_plural = "Images"


	def __str__(self):
		return f"{self.title}"
    



class ImagesHomePage(models.Model):
	photo = models.ImageField(upload_to="uploads/home_page/", blank=True, null = True)
	created = models.DateField(auto_now_add=True)
	title = models.CharField(max_length=30, default = "IMAGE")

	class Meta:
		verbose_name = "Home Image"
		verbose_name_plural = "Home Images"

	def __str__(self):
		return f"{self.title}"


