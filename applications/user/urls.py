from django.urls import path

from . import views

app_name = "user"


urlpatterns = [
	path('add/user/', 
		views.CreateUserFormView.as_view(), 
		name = "create_user"
	),
	
	path('settings/user/<int:pk>/', 
		views.SettingsUserTemplateView.as_view(), 
		name = 'settings-user'
	),
	path('update/user-email/<int:pk>/', 
		views.UpdateUserEmailFormView.as_view(), 
		name = "update-email-user"
	),
	path('update/user-photo/<int:pk>/', 
		views.UpdatePhotoUserView.as_view(),  
		name = 'update-photo-user'
	),
	path('update/user-password/<int:pk>/', 
		views.UpdatePasswordUser.as_view(),  
		name = 'update-password-user'
	),
	

	path('login/', views.LoginUserFormView.as_view(), name = "login"),
	path('logout/', views.LogoutUserView.as_view(), name = "logout"),
]
