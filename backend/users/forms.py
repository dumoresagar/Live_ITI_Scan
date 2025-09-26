from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput())


class UploadFileForm(forms.Form):
    file = forms.FileField(label="Upload Excel File")
    
class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','is_department', 'email','password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','is_department', 'email',]
        
        
class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField(label='Upload Excel File')


class DistrictUserUploadForm(forms.Form):
    excel_file = forms.FileField(label='Upload District Excel File')


class DigrUserUploadForm(forms.Form):
    excel_file = forms.FileField(label='Upload DIGR Excel File')
