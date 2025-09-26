from django.contrib import admin
from .models import *
from import_export.admin import ImportExportActionModelAdmin
# Register your models here.


@admin.register(Files)
class FilesAdmin(ImportExportActionModelAdmin,admin.ModelAdmin):
    list_display = (
        'filename', 
        'uploaded_by', 
        'uploaded_at', 
        'admin_approved',
        'dept_approved', 
        'district_rgtr_approved', 
        'digr_approved',
        'page_count'
    )
    list_filter = (
        'admin_approved',
        'dept_approved', 
        'district_rgtr_approved', 
        'digr_approved', 
        'uploaded_at'
    )
    
    search_fields = ('filename', 'uploaded_by__username')
    ordering = ('-uploaded_at',)
    
    
# Base Admin class with search functionality
class BaseAdmin(admin.ModelAdmin):
    search_fields = ('filename',)  # Enables search by filename

# Registering each model with the admin panel and search functionality
@admin.register(IndexFile)
class IndexFileAdmin(BaseAdmin):
    pass

@admin.register(MTPR)
class MTPRAdmin(BaseAdmin):
    pass

@admin.register(RHRegister)
class RHRegisterAdmin(BaseAdmin):
    pass

@admin.register(RegularDocumentRegister)
class RegularDocumentRegisterAdmin(BaseAdmin):
    pass

@admin.register(LoanOrderRegister)
class LoanOrderRegisterAdmin(BaseAdmin):
    pass

@admin.register(MemoOrderRegister)
class MemoOrderRegisterAdmin(BaseAdmin):
    pass

@admin.register(CourtOrderRegister)
class CourtOrderRegisterAdmin(BaseAdmin):
    pass