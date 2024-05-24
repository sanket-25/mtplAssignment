import pandas as pd
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .models import UploadFile
from django.core.files.storage import FileSystemStorage

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save()
            process_file(upload.file.path)
            return redirect('success')
    else:
        form = UploadFileForm()
    return render(request, 'fileupload/upload.html', {'form': form})

def success(request):
    return render(request, 'fileupload/success.html')

def process_file(filepath):
    try:
        df = pd.read_excel(filepath)
    except:
        df = pd.read_csv(filepath)
    
    required_columns = ['Date', 'ACCNO', 'Cust State', 'Cust Pin', 'DPD']
    if all(col in df.columns for col in required_columns):
        for index, row in df.iterrows():
            print(f"Date: {row['Date']}, ACCNO: {row['ACCNO']}, State: {row['Cust State']}, Pin: {row['Cust Pin']}, DPD: {row['DPD']}")
    else:
        print("Some required columns are missing")


def generate_summary_report(df):
    summary = {
        "shape": df.shape,
        "columns": df.columns.tolist(),
        "data_types": df.dtypes.apply(str).to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
        "head": df.head().to_html(classes='table table-striped'),
        "describe": df.describe(include='all').to_html(classes='table table-striped')
    }
    return summary

def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        filepath = fs.path(filename)
        try:
            # Try to read the file as an Excel file
            df = pd.read_excel(filepath)
            # Generate the summary report
            summary = generate_summary_report(df)
        except Exception as e:
            # Handle the error (e.g., show an error message)
            return render(request, 'upload.html', {'error': str(e)})
        return render(request, 'upload.html', {'summary': summary})
    return render(request, 'upload.html')