# employees/urls.py
from django.urls import path
from .views import register_employee, employee_list, read_nfc_uid, verify_employee,verify_employee_page


urlpatterns = [
    path('/register/', register_employee, name='register_employee'),
    path('', employee_list, name='employee_list'),
    path('/read_nfc_uid/', read_nfc_uid, name='read_nfc_uid'),
    path('/verify/', verify_employee, name='verify_employee'),
     path('/verify_page/', verify_employee_page, name='verify_employee_page'),
]
