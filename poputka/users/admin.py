from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin panel for custom User model with no username field"""

    fieldsets = (
        (None, {'fields': ('email',)}),
        (_('Personal info'), {'fields': ('first_name', 'birthday', 'avatar')}),
        (_('Permissions'), {'fields': ('is_verified' ,'is_active', 'is_staff', 'is_superuser',
                                      'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name',),
        }),
    )
    list_display = ('email', 'first_name',  'is_verified', 'is_staff')
    search_fields = ('email', 'first_name')
    ordering = ('email',)
