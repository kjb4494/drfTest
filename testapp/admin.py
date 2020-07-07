from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from testapp.forms.auth import CmbUserCreationForm, CmbUserChangeForm

from testapp.models import CmbUser, Modifier, UserHasModifier, Country


# Register your models here.
class CmbUserAdmin(UserAdmin):
    form = CmbUserChangeForm
    add_form = CmbUserCreationForm

    list_display = ('idx', 'username', 'country', 'point', 'reg_date', 'last_login')
    list_display_links = ('username',)
    list_filter = ('country',)
    fieldsets = (
        (None, {'fields': ('country', 'point')}),
    )
    add_fieldsets = (
        (None, {'fields': ('username', 'password', 'password_confirm', 'country', 'point')}),
    )
    ordering = ('-last_login',)
    filter_horizontal = ()
    search_fields = ('username', 'country')


admin.site.site_header = 'EuropaIV CMB Admin'
admin.site.site_title = 'Admin Page'
admin.site.index_title = 'EuropaIV CMB'

admin.site.register(CmbUser, CmbUserAdmin)
admin.site.register(Modifier)
admin.site.register(UserHasModifier)
admin.site.register(Country)