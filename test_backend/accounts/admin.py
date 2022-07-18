from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

from accounts.models import UserProfile
from .models import User, PolarisUser, PolarisStellarAccount, PolarisUserTransaction


class ProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "User's Profile"
    list_display = "id"


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""
    inlines = (ProfileInline,)
    readonly_fields = ('date_joined', 'unique_id')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),

    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'nickname',
                    'date_joined', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'nickname',
                     'date_joined', 'first_name', 'last_name')
    ordering = ('email',)


class PolarisUserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "tontine_user",
        'bank_account_number',
        'bank_number'
    )


class PolarisStellarAccountAdmin(admin.ModelAdmin):
    list_display = "user", "account", "confirmed"


class PolarisUserTransactionAdmin(admin.ModelAdmin):
    list_display = "transaction_id", "account", "user"


admin.site.register(PolarisUser, PolarisUserAdmin)
admin.site.register(PolarisStellarAccount, PolarisStellarAccountAdmin)
admin.site.register(PolarisUserTransaction, PolarisUserTransactionAdmin)
