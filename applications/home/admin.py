from django.contrib import admin

from . import models
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
	list_display = [
		'id',
		'name'
	]


class ImageAdmin(admin.ModelAdmin):
	list_display = [
		"id",
		'title',
	]


class ImagesHomePageAdmin(admin.ModelAdmin):
	list_display = [
		"id",
		'title',
	]




admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Image, ImageAdmin)
admin.site.register(models.ImagesHomePage, ImagesHomePageAdmin)

