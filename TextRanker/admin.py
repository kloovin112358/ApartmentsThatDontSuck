from django.contrib import admin
from .models import *

class CustomUserAdmin(admin.ModelAdmin):
    # Remove 'username' from ordering and list_filter
    ordering = ['email']
    list_filter = ['email', 'is_active', 'verified_account', 'account_banned']
    
    # Ensure the fields in 'fields' and 'fieldsets' reflect the current model
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('verified_account', 'account_banned', 'ban_datetime', 'ban_removal_datetime', 'ban_reason')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    # Ensure 'list_display' reflects the current model
    list_display = ('email', 'verified_account', 'is_active', 'account_banned', 'date_joined', 'last_login')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(DisposableEmailDomain)
admin.site.register(Neighborhood)
admin.site.register(ListingSite)
admin.site.register(UnitType)
admin.site.register(Unit)
admin.site.register(UnitSucksReport)
admin.site.register(UnitNotAvailableReport)
admin.site.register(Search)
admin.site.register(SavedUnit)
admin.site.register(QualityValuePriceMinMax)
admin.site.register(QualityRating)
admin.site.register(QualityValue)