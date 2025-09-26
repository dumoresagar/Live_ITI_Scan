import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
from .models import RegularDocumentRegister, MTPR
from django.core.exceptions import ValidationError
from django.shortcuts import redirect

def upload_regular_document(request):
    if request.method == 'POST' and request.FILES['file']:
        excel_file = request.FILES['file']
        
        # Load the Excel file using pandas
        try:
            data = pd.read_excel(excel_file, engine='openpyxl')
        except Exception as e:
            return HttpResponse(f"Error reading Excel file: {str(e)}")

        # Prepare a list of filenames to check for duplicates
        new_filenames = []
        instances = []
        
        for _, row in data.iterrows():
            office_code = str(row['Office Code']).zfill(3)  # Ensures leading zeros
            book_no = str(row['Book Number']).zfill(2)  # Ensures leading zeros
            running_no = str(row['Document Number']).zfill(2)  # Ensures leading zeros
            year = row['Year']

            # Construct the filename according to the naming convention
            filename = f"R_{office_code}_{book_no}_{running_no}_{year}"
            new_filenames.append(filename)

            # Create an instance but don't save it yet
            instances.append(
                RegularDocumentRegister(
                    filename=filename,
                    submitted=False,  # Default status
                    approved=False  # Default status
                )
            )
        
        # Check which filenames already exist in the database
        existing_filenames = set(
            RegularDocumentRegister.objects.filter(filename__in=new_filenames).values_list('filename', flat=True)
        )
        
        # Filter out instances with duplicate filenames
        unique_instances = [instance for instance in instances if instance.filename not in existing_filenames]
        
        # Bulk create only the unique instances
        RegularDocumentRegister.objects.bulk_create(unique_instances)

        # Redirect to a success page or show a success message
        return HttpResponse("Uploaded Succssss") # Replace with actual URL

    return render(request, 'documents/upload_regular_document.html')  # Adjust with actual template


def upload_mtpr(request):
    if request.method == 'POST' and request.FILES['file']:
        excel_file = request.FILES['file']

        try:
            data = pd.read_excel(excel_file, engine='openpyxl')
        except Exception as e:
            return HttpResponse(f"Error reading Excel file: {str(e)}")

        instances = []
        for _, row in data.iterrows():
            office_code = str(row['Office Code']).zfill(3)
            volume_no = str(row['Volume No']).zfill(2)
            part = f"p{str(row['Part Number'])}"  # Assuming part column is available

            filename = f"MTPR_{office_code}_{volume_no}_{part}"

            instances.append(
                MTPR(
                    filename=filename,
                    submitted=False,
                    approved=False
                )
            )

        MTPR.objects.bulk_create(instances)

        return redirect('success_url')

    return render(request, 'upload_mtpr.html')
