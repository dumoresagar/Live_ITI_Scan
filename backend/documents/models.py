from django.db import models
from users.models import Agency, Office
from PIL import Image
import os
import re


# Create your models here.
class IndexFile(models.Model):
    filename = models.CharField(max_length=255, blank=True, unique=True)
    submitted = models.BooleanField(null=True,blank=True)
    approved = models.BooleanField(null=True,blank=True)
    

class MTPR(models.Model):
    filename = models.CharField(max_length=255, blank=True, unique=True)
    submitted = models.BooleanField(null=True,blank=True)
    approved = models.BooleanField(null=True,blank=True)
    
    def __str__(self):
        return self.filename
    
    
class RHRegister(models.Model):
    filename = models.CharField(max_length=255, blank=True, unique=True)
    submitted = models.BooleanField(null=True,blank=True)
    approved = models.BooleanField(null=True,blank=True)
    
    def __str__(self):
        return self.filename

class RegularDocumentRegister(models.Model):
    filename = models.CharField(max_length=255, blank=True, unique=True)
    submitted = models.BooleanField(null=True,blank=True)
    approved = models.BooleanField(null=True,blank=True)
    
    def __str__(self):
        return self.filename

class LoanOrderRegister(models.Model):
    filename = models.CharField(max_length=255, blank=True, unique=True)
    submitted = models.BooleanField(null=True,blank=True)
    approved = models.BooleanField(null=True,blank=True)
    
    def __str__(self):
        return self.filename

class MemoOrderRegister(models.Model):
    filename = models.CharField(max_length=255, blank=True, unique=True)
    submitted = models.BooleanField(null=True,blank=True)
    approved = models.BooleanField(null=True,blank=True)
    
    def __str__(self):
        return self.filename

class CourtOrderRegister(models.Model):
    filename = models.CharField(max_length=255, blank=True, unique=True)
    submitted = models.BooleanField(null=True,blank=True)
    approved = models.BooleanField(null=True,blank=True)
    
    def __str__(self):
        return self.filename



class Files(models.Model):
    office = models.ForeignKey(Office, on_delete=models.SET_NULL,null=True,blank=True)
    processed_file = models.FileField(upload_to='processed_files/')
    filename = models.CharField(max_length=255, blank=True, unique=True)
    uploaded_by = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='uploaded_files')
    uploaded_at = models.DateTimeField(null=True, blank=True)
    processed = models.BooleanField(default=False)
    remark = models.CharField(max_length=255, null=True, blank=True)
    remark_by_scanner = models.CharField(max_length=255, null=True, blank=True)
    send_to_sro = models.BooleanField(default=False)
    send_to_qc = models.BooleanField(default=False)

    admin_approved = models.BooleanField(null=True, blank=True)
    admin_approved_by =  models.ForeignKey('users.User', on_delete=models.CASCADE, null=True, blank=True, related_name='approved_admin')
    admin_approved_at = models.DateTimeField(null=True, blank=True)

    
    dept_approved = models.BooleanField(null=True, blank=True)
    dept_approved_by = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True, blank=True, related_name='approved_files')
    dept_approved_at = models.DateTimeField(null=True, blank=True)
    
    district_rgtr_approved = models.BooleanField(null=True,blank=True)
    district_rgtr_approved_by = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True, blank=True, related_name='district_rgtr_approved_by')
    district_rgtr_approved_at = models.DateTimeField( null=True, blank=True)
    
    digr_approved = models.BooleanField(null=True,blank=True)
    digr_approved_by = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True, blank=True, related_name='digr_approved')
    digr_approved_at = models.DateTimeField( null=True, blank=True)

    page_count = models.PositiveIntegerField(null=True, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['uploaded_at']),
            models.Index(fields=['office']),
        ]

    
    def normalize_filename(self, raw_name):
        name = os.path.splitext(os.path.basename(raw_name))[0]

        patterns = [
            r"^(I_\d{1,3}_\d+_\d{4}_\d+)", 
            r"^(MTPR_\d{1,3}_\d+)",  
            r"^(RH_\d{1,3}_\d+)", 
            r"^((R|LO|MO|CO)_\d{1,3}_\d+_\d+_\d{4})",     
        ]

        for pattern in patterns:
            match = re.match(pattern, name, re.IGNORECASE)
            if match:
                return match.group(1)
        return name
    
    def save(self, *args, **kwargs):
        if self.processed_file:
            raw_name = self.processed_file.name
            base_name = self.normalize_filename(raw_name)
            cleaned_name = base_name.replace('_processed', '')
            self.filename = cleaned_name

            # Check for duplicates and delete older entry (excluding self)
            try:
                existing = Files.objects.get(filename=cleaned_name)
                if existing.pk != self.pk:
                    existing.processed_file.delete(save=False)
                    existing.delete()
            except Files.DoesNotExist:
                pass

            # Count pages if possible
            try:
                self.processed_file.seek(0)
                with Image.open(self.processed_file) as img:
                    self.page_count = getattr(img, 'n_frames', 1)
            except Exception:
                self.page_count = 1

        super().save(*args, **kwargs)


    def extract_filename(self, file_name):
        import re
        # Regex to extract the relevant part of the filename
        match = re.match(r"([A-Za-z0-9_]+(?:_\d+){3,4})", file_name)
        return match.group(0) if match else file_name
    
    def __str__(self):
        return f'{self.filename}'
    
    def get_year(self):
        return self.filename[-4:]
    
class ReceivedDocuments(models.Model):
    date  = models.DateField(auto_now_add=True)
    document_type = models.CharField(max_length=5,null=True,blank=True)
    index_type = models.CharField(max_length=5,null=True,blank=True)
    received = models.IntegerField(null=True,blank=True)
    uploaded = models.IntegerField(null=True,blank=True)
    remark = models.CharField(max_length=255,null=True,blank=True)
    agency = models.ForeignKey(Agency, on_delete=models.SET_NULL, null=True,blank=True)
    created_by =  models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='received_files')


    def __str__(self):
        return self.document_type