from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.admin import SimpleListFilter
# Register your models here.

class UserAdmin(BaseUserAdmin):
    # Define which fields to be displayed in the list view
    list_display = ('id','username', 'email', 'first_name', 'last_name', 'is_department')
    list_filter = ( 'is_active',)

    # Define the fieldsets for the detail view
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name','avatar','last_name', 'email','contact', 'office','district','zone','is_admin','agency')}),
        ('Permissions', {'fields': ('is_district_rgtr','is_department','is_digr','is_agency_admin', 'is_active','is_agency_qc_employee','is_agency_scanning_employee')}),
    )

    # Override to use the custom user model's fields
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_department')}
        ),
    )

    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)

@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    search_fields = ['zone_name', 'zone_code', 'office_name']
    list_display = ['zone_name', 'zone_code', 'office_name', 'address']

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    search_fields = ['district_name', 'district_code']
    list_display = ['district_name', 'district_code', 'zone']

@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    search_fields = ['office_name', 'office_code']
    list_display = ['office_name', 'office_code', 'district']
    
admin.site.register(Agency)


class ActivityCategoryFilter(SimpleListFilter):
    title = 'Activity Category'
    parameter_name = 'category'

    def lookups(self, request, model_admin):
        return (
            ('success', 'Success'),
            ('danger', 'Danger'),
            ('primary', 'Primary'),
            ('info', 'Info'),
            ('warning', 'Warning'),
            ('muted', 'Muted'),
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(category=self.value())
        return queryset


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp', 'ip_address', 'device_type', 'browser', 'os', 'category')
    search_fields = ('user__username', 'action', 'ip_address', 'browser', 'os')
    list_filter = (ActivityCategoryFilter, 'timestamp', 'device_type', 'browser', 'os')
