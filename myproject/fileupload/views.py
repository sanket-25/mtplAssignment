import pandas as pd
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .models import UploadFile

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
