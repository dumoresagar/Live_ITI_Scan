from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.



class Zone(models.Model):
    zone_name = models.CharField(max_length=20,null=True, blank=True)
    zone_code = models.CharField(max_length=20,null=True, blank=True)
    office_name = models.CharField(max_length=10,null=True, blank=True)
    address = models.CharField(max_length=300,null=True,blank=True)

    def __str__(self):
        return self.zone_name


class District(models.Model):
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name='districts')
    district_code = models.CharField(max_length=20,null=True, blank=True)
    
    district_name = models.CharField(max_length=20)
    address = models.CharField(max_length=300,null=True,blank=True)

    def __str__(self):
        return self.district_name


class Office(models.Model):
    district = models.ForeignKey('District', on_delete=models.CASCADE, related_name='offices')
    office_name = models.CharField(max_length=50)
    office_code = models.CharField(max_length=20,null=True, blank=True)
    
    address = models.CharField(max_length=300,null=True,blank=True)

    def __str__(self):
        return self.office_name


class Agency(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(null=True, blank=True)
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    office = models.ForeignKey(Office, on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.name
    
    
    
class User(AbstractUser):
    is_department = models.BooleanField(default=False,null=True,blank=True)
    office = models.ForeignKey(Office, on_delete=models.CASCADE,null=True,blank=True)
    
    is_district_rgtr = models.BooleanField(default=False,null=True,blank=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True, blank=True)
    
    is_digr = models.BooleanField(default=False,null=True,blank=True)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, null=True, blank=True)
    
    is_admin = models.BooleanField(default=False,null=True,blank=True)
    
    
    is_active = models.BooleanField(default=True)
    avatar = models.ImageField(upload_to='uploads/userprofile', null=True, blank=True)
    
    contact = models.CharField(max_length=15,null=True,blank=True)
    
    is_igr = models.BooleanField(null=True,blank=True)
    
    is_agency = models.BooleanField(default=False, null=True, blank=True)
    is_agency_admin = models.BooleanField(default=False, null=True, blank=True)
    is_agency_qc_employee = models.BooleanField(default=False, null=True, blank=True)
    is_agency_scanning_employee = models.BooleanField(default=False, null=True, blank=True)
    
    agency = models.ForeignKey('Agency', on_delete=models.CASCADE, null=True, blank=True)
    

    
    def __str__(self):
        return f"{self.pk},{self.username}"
    
    
    def get_avatar(self):
        if self.avatar:
            return self.avatar.url
        else:
            return '/static/assets/img/avatar.png'
        
        
class UserActivity(models.Model):
    CATEGORY_CHOICES = [
        ('success', 'Success'),
        ('danger', 'Danger'),
        ('primary', 'Primary'),
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('muted', 'Muted'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="activities")
    action = models.CharField(max_length=255) 
    timestamp = models.DateTimeField(auto_now_add=True) 
    ip_address = models.GenericIPAddressField(blank=True, null=True) 
    device_type = models.CharField(max_length=10, blank=True, null=True) 
    browser = models.CharField(max_length=50, blank=True, null=True)
    os = models.CharField(max_length=50, blank=True, null=True) 
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='info')
    details = models.TextField(blank=True, null=True) 

    class Meta:
        ordering = ['-timestamp'] 

    def __str__(self):
        return f"{self.user.username}: {self.action} at {self.timestamp} from {self.device_type} ({self.browser})"
    
    @property
    def formatted_timestamp(self):
        # Convert to local timezone
        local_time = timezone.localtime(self.timestamp)

        # Get the day without leading zero
        day = local_time.day

        # Format the rest of the date and time
        formatted = local_time.strftime("%b %Y %I:%M %p").lower()

        # Remove a possible leading zero from the hour
        if formatted[0] == '0':
            formatted = formatted[1:]

        return f"{day} {formatted}"