from rest_framework import serializers
from .models import *
from django.utils import timezone
from users.models import Office, UserActivity
import os
import re
from django.core.files.storage import default_storage
from rest_framework.exceptions import ValidationError




OFFICE_CODE_PATTERNS = [
    r"^I_(\d{1,3})_",        # Index File
    r"^MTPR_(\d{1,3})_",     # Municipal Town Property Register
    r"^RH_(\d{1,3})_",       # Register of Holdings
    r"^R_(\d{1,3})_",        # Regular Document Register
    r"^LO_(\d{1,3})_",       # Loan Order Register
    r"^MO_(\d{1,3})_",       # Memo Order Register
    r"^CO_(\d{1,3})_"        # Court Order Register
]

def extract_office_code(filename):
    """Extracts the Office Code from the filename using regex patterns."""
    for pattern in OFFICE_CODE_PATTERNS:
        match = re.match(pattern, filename)
        if match:
            return match.group(1).zfill(3)  # Ensure 3-digit format
    return None


class FilesUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = ['id', 'processed_file', 'filename', 'uploaded_at', 'processed', 'page_count']
        read_only_fields = ['filename', 'uploaded_at', 'processed', 'page_count']

    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        file = validated_data['processed_file']
        filename = os.path.splitext(file.name)[0]
        office_code = extract_office_code(filename)
        office = Office.objects.filter(office_code=office_code).first() if office_code else None
        
        if office is None:
            raise ValidationError({"office": f"No office found for file '{filename}' with code '{office_code}'."})


        existing_file = Files.objects.filter(filename=filename).first()
        ip = getattr(request, 'ip_address', 'unknown')
        device_type = getattr(request, 'device_type', '')
        browser = getattr(request, 'browser', '')
        os_info = getattr(request, 'os', '')

        if existing_file:
            # Delete old file if exists
            if existing_file.processed_file:
                old_path = existing_file.processed_file.path
                if default_storage.exists(old_path):
                    default_storage.delete(old_path)

            # Update fields based on admin status
            existing_file.processed_file = file
            existing_file.uploaded_at = timezone.now()
            existing_file.uploaded_by = user
            existing_file.processed = True
            existing_file.office = office or existing_file.office
            existing_file.admin_approved = user.is_admin or None
            existing_file.dept_approved = None
            existing_file.send_to_qc = not user.is_admin
            existing_file.send_to_sro = user.is_admin
            existing_file.district_rgtr_approved = None
            existing_file.digr_approved = None
            existing_file.save()

            UserActivity.objects.create(
                user=user, action=f"Replaced file '{filename}'", category="info",
                ip_address=ip, device_type=device_type, browser=browser, os=os_info
            )

            return existing_file

        else:
            file_instance = Files.objects.create(
                processed_file=file,
                filename=filename,
                uploaded_by=user,
                processed=True,
                uploaded_at=timezone.now(),
                office=office,
                admin_approved=user.is_admin or None,
                send_to_qc=not user.is_admin,
                send_to_sro=user.is_admin
            )

            UserActivity.objects.create(
                user=user, action=f"Uploaded new file '{filename}'", category="success",
                ip_address=ip, device_type=device_type, browser=browser, os=os_info
            )

            return file_instance