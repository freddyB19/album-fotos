from django.urls import path

from . import views

app_name = "home"

urlpatterns = [
	path("index/", views.IndexView.as_view(), name = "index"),
	
	path(
		"add/category/<int:pk>/", 
		views.NewCategoryFormView.as_view(), 
		name = "add-category"
	),
	path(
		'list/user-categorys/',
		views.AllCategoryListView.as_view(),
		name = 'list-categorys'
	),
	path(
		'detail/<slug>/<int:pk>/',
		views.CategoryDetailView.as_view(),
		name = 'detail-categorys'
	),
	path(
		'update/category-name/<int:pk>/',
		views.CategoryNameUpdate.as_view(),
		name = 'update-category-name'
	),
	path(
		'update/category-status/<int:pk>/',
		views.CategoryStatusUpdateView.as_view(),
		name = 'update-status-name'
	),
	path(
		'delete/category/<int:pk>/',
		views.CategoryDeleteView.as_view(),
		name = 'delete-category'
	),
	

	path(
		'add/user-photo/',
		views.SaveImageView.as_view(),
		name = 'add-photo'
	),
	path(
		'user-photo/<int:pk>/detail',
		views.ImageDetailView.as_view(),
		name = 'detail-photo'
	),
	path(
		'user-photo/<int:pk>/update/',
		views.UpdateImageView.as_view(),
		name = 'update-photo'
	),
	path(
		'user-photo/<int:pk>/delete/',
		views.ImageDeleteView.as_view(),
		name = 'delete-photo'
	),
	
	
]


