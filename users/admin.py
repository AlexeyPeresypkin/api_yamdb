from django.contrib import admin

from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'first_name',
        'last_name',
        'username',
        'bio',
        'email',
        'role',
    )
    readonly_fields = ('last_login',)


admin.site.register(User, UserAdmin)
