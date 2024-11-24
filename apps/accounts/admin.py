from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Personalization

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined', 'last_login']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)


@admin.register(Personalization)
class PersonalizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'difficulty')
    search_fields = ('user__username', 'personal_details')
    list_filter = ('difficulty',)
    readonly_fields = ('id',)

    fieldsets = (
        (None, {
            'fields': ('user', 'difficulty', 'personal_details')
        }),
    )