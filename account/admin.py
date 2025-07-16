from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import User


class UserModelAdmin(UserAdmin):
	model = User
	list_display = ('id', 'email', 'name', 'is_superuser', 'is_active', 'is_staff', 'is_customer', 'is_seller')
	list_filter = ['is_superuser']
	fieldsets = [
		('User credentials', {'fields': ['email', 'password']}),
		('User Informations', {'fields': ['name']}),
		('Permissions', {'fields': ['is_superuser', 'is_active', 'is_staff', 'is_customer', 'is_seller']})
	]
	add_fieldsets = [
		(
			None,
			{
				'classes': ['wide'],
				'fields': ['email', 'name', 'password1', 'password2'],
			},
		),
	]
	search_fields = ('email',)
	ordering = ('email', 'id')
	filter_horizontal = []


admin.site.register(User, UserModelAdmin)