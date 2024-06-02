# employees/views.py
import nfc
import threading
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

nfc_uid = None

def read_nfc():
    global nfc_uid
    def on_connect(tag):
        global nfc_uid
        nfc_uid = tag.identifier.hex().upper()
        return False
    
    clf = nfc.ContactlessFrontend('usb')
    clf.connect(rdwr={'on-connect': on_connect})

@csrf_exempt
def read_nfc_uid(request):
    global nfc_uid
    nfc_uid = None
    # Run the NFC reader in a separate thread to avoid blocking
    thread = threading.Thread(target=read_nfc)
    thread.start()
    thread.join(timeout=5)  # Wait for 5 seconds for the NFC UID to be read
    if nfc_uid:
        return JsonResponse({'nfc_uid': nfc_uid})
    else:
        return JsonResponse({'error': 'Failed to read NFC UID'})


# employees/views.py
from django.shortcuts import render, redirect
from .forms import EmployeeForm
from .models import Employee

def register_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'employees/register_employee.html', {'form': form})

def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employees/employee_list.html', {'employees': employees})

def verify_employee_page(request):
    return render(request, 'employees/verify_employee.html')

# employees/views.py
from django.http import JsonResponse

@csrf_exempt
def verify_employee(request):
    if request.method == 'POST':
        nfc_uid = request.POST.get('nfc_uid')
        try:
            employee = Employee.objects.get(nfc_uid=nfc_uid)
            return JsonResponse({'status': 'success', 'employee': employee.name})
        except Employee.DoesNotExist:
            return JsonResponse({'status': 'failure', 'message': 'Employee not found'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


# # employees/views.py
# from django.shortcuts import render
# from django.http import JsonResponse

# def verify_employee_page(request):
#     return render(request, 'employees/verify_employee.html')

# @csrf_exempt
# def verify_employee(request):
#     if request.method == 'POST':
#         nfc_uid = request.POST.get('nfc_uid')
#         try:
#             employee = Employee.objects.get(nfc_uid=nfc_uid)
#             return JsonResponse({'status': 'success', 'employee': {'name': employee.name, 'email': employee.email}})
#         except Employee.DoesNotExist:
#             return JsonResponse({'status': 'failure', 'message': 'Employee not found'})
#     return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
