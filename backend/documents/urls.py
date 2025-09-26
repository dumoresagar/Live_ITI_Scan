from django.urls import path
from .views import *
from .upload import upload_regular_document

urlpatterns = [
    
    path('upload_processed_api/', UploadTiffFileView.as_view(), name='upload-tiff'),
    
    # Scan user URLS
    path('upload_processed_files/', upload_processed_files, name='upload_processed_files'),
    path('processed_files/', processed_files, name='processed_files'),
    
    path('admin_approve_file/<int:file_id>/', admin_approve_file, name='admin_approve_file'),
    
    
    path('send_to_sro/', send_to_sro, name='send_to_sro'),
    path('send_to_qc/', send_to_qc, name='send_to_qc'),
    
    
    path('file/<int:file_id>/', file, name='file'),
    path('scanned_files/', scanned_files, name='scanned_files'),
    path('igr_report/', igr_report, name='igr_report'),
    path('download_sro_report/', download_sro_report, name='download_sro_report'),
    path('download_district_report/', download_district_report, name='download_district_report'),
    path('download_zone_report/', download_zone_report, name='download_zone_report'),

    path('zone_wise_report/', zone_wise_report, name='zone_wise_report'),

    path('self_approved_files_sro_excel/', self_approved_files_sro_excel, name='self_approved_files_sro_excel'),


    
    # path('upload_unprocessed_files/', upload_unprocessed_files, name='upload_unprocessed_files'),
    
    # SRO URLS 
    path('files_for_qc/', files_for_qc, name='files_for_qc'),
    path('processed_file/<int:file_id>/', processed_file, name='processed_file'),
    path('approve_file/<int:file_id>/', approve_file, name='approve_file'),
    path('self_approved_files_sro/', self_approved_files_sro, name='self_approved_files_sro'),
    
    
    # DR URLS 
    path('sro_approved_files/', sro_approved_files, name='sro_approved_files'),
    path('sro_approved_file/<int:file_id>/', sro_approved_file, name='sro_approved_file'),
    path('approve_file_district_admin/<int:file_id>/', approve_file_district_admin, name='approve_file_district_admin'),
    path('rejected_by_dist_a/', rejected_by_dist_a, name='rejected_by_dist_a'), 
    
    # DIGR URLS
    path('d_a_approved_files/', d_a_approved_files, name='d_a_approved_files'),
    path('d_a_approved_file/<int:file_id>/', d_a_approved_file, name='d_a_approved_file'),
    path('approve_file_digr/<int:file_id>/', approve_file_digr, name='approve_file_digr'),
    path('rejected_by_digr/', rejected_by_digr, name='rejected_by_digr'), 
    
    
    
    path('approve_rejected_file/<int:file_id>/', approve_rejected_file, name='approve_rejected_file'),
    
    
    # OTHER URLS agency_wise_users_data
    
    path('agency_wise_users_data/<int:user_id>/', agency_wise_users_data, name='agency_wise_users_data'),
    
    
    path('rejected_file/<int:file_id>/', rejected_file, name='rejected_file'),
    path('rejected_files/', rejected_files, name='rejected_files'),

    path('approved_files/', approved_files, name='approved_files'),
    path('approved_file/<int:file_id>/', approved_file, name='approved_file'),
    
    path('download_file/<int:file_id>/', download_file, name='download_file'),
    path("download-selected-files/", download_selected_files, name="download_selected_files"),

    path('download-report/', download_excel_report, name='download_report'),
    path('all_dept_approved_files/', all_dept_approved_files, name='all_dept_approved_files'),
    path('final_file/<int:file_id>/', final_file, name='final_file'),
    
    
    path('overall_report/', overall_report, name='overall_report'),
    path('download_sro_rejected_files/', download_rejected_files_excel, name='download_sro_rejected_files'),
    
    path('agency_user_wise_data_download/', zip_download_view, name='agency_user_wise_data_download'),

    
    
    # UPLOAD 
    path('upload_regular_document/', upload_regular_document, name='upload_regular_document'),
    path('add_received_docs/', add_received_docs, name='add_received_docs'),

    path('remove/', remove, name='remove'),
    
    path('export-files/', AllOfficesZipExportView.as_view(), name='export-files'),
    path('download-files/', FilePathDocumentDownloadURL.as_view(), name='download-files'),
    path('export-dept-approval/', export_dept_approval_excel, name='export_dept_approval'),
    path('download/approved-zip/', download_dept_approved_zip, name='download_approved_zip'),

    


    

]