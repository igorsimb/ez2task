from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User, Profile, Department, Company

from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils.translation import gettext_lazy as _


# bulk add users to Company 1
# co_1 = Company.objects.get(id=1)

# @admin.action(description=f"Add users to {co_1.name}")
# def add_to_company_1(modeladmin, request, queryset):
#     queryset.update(company_id=1)


# bulk add users to Company 2
# co_2 = Company.objects.get(id=2)
#
# @admin.action(description=f"Add users to {co_2.name}")
# def add_to_company_2(modeladmin, request, queryset):
#     queryset.update(company_id=2)


class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'company', 'account_type', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'username')
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    # actions = [add_to_company_1, add_to_company_2]

# Custom user creation form in admin site to include email field
# SOURCE: https://gist.github.com/riklomas/511440

class UserCreationFormExtended(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationFormExtended, self).__init__(*args, **kwargs)
        self.fields['email'] = forms.EmailField(label=_("E-mail"), max_length=75)
        self.fields['username'] = forms.CharField(label=_("Name"), max_length=150)


UserAdmin.add_form = UserCreationFormExtended
UserAdmin.add_fieldsets = (
    (None, {
        'classes': ('wide',),
        'fields': ('email', 'username', 'password1', 'password2', 'company')  # 'department' currently not available
    }),
)


# Users TabularInline
class UserInline(admin.TabularInline):
    model = User
    fields = ('username',)


class CompanyAdmin(admin.ModelAdmin):
    inlines = [UserInline]

    class Meta:
        model = Company


admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)
admin.site.register(Department)
admin.site.register(Company, CompanyAdmin)