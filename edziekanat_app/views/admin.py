import datetime

from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render

from ..forms import SystemTools, AddChair, AddDepartment, AddFaculty, AddCourse, AddEmployee, AddInvoiceCategory, \
    AddInvoiceField, AddInvoice, AddJob, AddMessage, AddRole, AddSpectialization, AddStudyMode, AddStudent, AddSubject
from ..models.tables.messages.message import Message
from ..models.tables.users.user import User


def tools(request):
    form = SystemTools()
    if request.method == "POST":
        title = request.POST.get('title')
        text = request.POST.get('broadcast')
        if title is not None and text is not None:
            users = User.objects.filter(~Q(id=request.user.id))
            for user in users:
                Message.objects.create(
                    sender=request.user,
                    reciever=user,
                    seen=False,
                    message_text=text,
                    message_title=title,
                    created_date=datetime.datetime.now()
                ).save()
            messages.success(request, f"Wysłano wiadomość do {users.count()} użytkowników.")

    return render(request, 'admin/tools.html', context={'form': form, 'toolname': 'Wiadomość broadcast'})


def database(request):
    if request.method == 'GET':
        form_chair = AddChair()
        form_department = AddDepartment()
        form_faculty = AddFaculty()
        form_course = AddCourse()
        form_employee = AddEmployee()
        form_invoice_categorie = AddInvoiceCategory()
        form_invoice_field = AddInvoiceField()
        form_invoice = AddInvoice()
        form_job = AddJob()
        form_message = AddMessage()
        form_role = AddRole()
        form_spectialization = AddSpectialization()
        form_student = AddStudent()
        form_study_mode = AddStudyMode()
        form_subject = AddSubject()
        return render(request, 'admin/database.html',
                      {'form_chair': form_chair, 'form_department': form_department, 'form_faculty': form_faculty,
                       'form_course': form_course, 'form_employee': form_employee,
                       'form_invoice_categorie': form_invoice_categorie,
                       'form_invoice_field': form_invoice_field, 'form_invoice': form_invoice, 'form_job': form_job,
                       'form_message': form_message, 'form_role': form_role,
                       'form_spectialization': form_spectialization,
                       'form_student': form_student, 'form_study_mode': form_study_mode, 'form_subject': form_subject})
    elif request.method == 'POST':
        raise Exception("Not implemented")
    return render(request, 'admin/database.html')
