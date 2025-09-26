from django.urls import path
from .views import (
    login_view,logout_view,dashboard,profile_user,users, upload_digr_excel,agencies,create_agencies_view,agency_users,create_agency_user_view,LoginView,reports_dasboards,
    create_user_view,update_user_view,filtered_data_view,upload_excel,igr_dashboard,upload_excel_sro,upload_district_excel,upload_excel_srocode,export_agency_report_excel,
    office_wise_page_report,update_existing_files_page_count,activities_get,download_activities_excel,create_agency_qc_users_excel, agency_wise_report
)

urlpatterns = [
    path('', login_view, name='login'),
    path('login/', LoginView.as_view()),
    path('logout/', logout_view, name='logout'),
    path('generate_agency_users_excel/', create_agency_qc_users_excel, name='generate_agency_users_excel'),
     

    path('dashboard/', dashboard, name='dashboard'),
    path('update_existing_files_page_count/', update_existing_files_page_count, name='update_existing_files_page_count'),

    path('profile/', profile_user, name='profile'),
    
    path('users/', users, name='users'),
    path('agency_users/', agency_users, name='agency_users'),
    
    path('agencies/', agencies, name='agencies'),
    
    
    path('user/<int:user_id>/', update_user_view, name='user'),
    
    path('create_agency/', create_agencies_view, name='create_agency'),
    
    path('create_user/', create_user_view, name='create_user'),
    path('create_agency_user/', create_agency_user_view, name='create_agency_user'),
    
    
    path('filtered-data/', filtered_data_view, name='filtered_data_page'),
    
    path('igr_dash/', igr_dashboard, name='igr_dash'),
    
    
    path('upload_excel/', upload_excel, name='upload_excel'),
    path('upload_excel_sro/', upload_excel_sro, name='upload_excel_sro'),
    path('upload_district_excel/', upload_district_excel, name='upload_district_excel'),
    path('upload_digr_excel/', upload_digr_excel, name='upload_digr_excel'),
    path('upload_excel_srocode/', upload_excel_srocode, name='upload_excel_srocode'),
    path("office_wise_page_report/", office_wise_page_report, name="office_wise_page_report"),
    path("activities/", activities_get, name="activities"),
    path("download_activities_excel/", download_activities_excel, name="download_activities_excel"),
    path('agency_wise_report/<int:agency_id>/',agency_wise_report,name='agency_wise_report'),
    path('export_agency_report_excel/<int:agency_id>/export/', export_agency_report_excel, name='export_agency_report_excel'),
    path('reports/',reports_dasboards,name='reports')


]