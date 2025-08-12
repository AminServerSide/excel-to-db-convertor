# teeeest/apps/views.py
from django.shortcuts import render
from django.http import HttpResponse
from .forms import ExcelUploadForm
from .management.commands.import_excel import import_excel_to_db

def upload_excel(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            # Save the uploaded file temporarily
            with open('temp_excel.xlsx', 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            # Call the import function
            try:
                result = import_excel_to_db('temp_excel.xlsx')
                return HttpResponse(result)
            except Exception as e:
                return HttpResponse(f"Import failed: {str(e)}")
        else:
            return HttpResponse("Invalid form submission")
    else:
        form = ExcelUploadForm()
    return render(request, 'apps/upload.html', {'form': form})