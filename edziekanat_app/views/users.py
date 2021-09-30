import datetime

from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect, render
from formtools.wizard.views import SessionWizardView

from edziekanat_app.forms import EditUserForm, LoginForm
from edziekanat_app.models.tables.users.employee import Employee
from edziekanat_app.models.tables.users.student import Student
from edziekanat_app.models.tables.users.user import User
from django.contrib.auth.views import auth_logout


def user_login(request):
    template = 'auth/login.html'

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            print(user)
            if user is not None:
                login(request, user)
                print(f"Zalogowano:\n"
                      f"Email:{user.email}\n"
                      f"Hasło:{user.password}\n"
                      f"Imie:{user.first_name}\n"
                      f"Nazwisko:{user.last_name}")
                messages.success(request, "Pomyślnie zalogowano!")

                return redirect('/')
            else:
                messages.error(request, 'Podano nieprawidłowe dane logowania.')
                return render(request, 'auth/login.html', {
                    'form': form,
                })
    else:
        form = LoginForm()

    return render(request, template, {'form': form, "time": datetime.datetime.now()})


def user_logout(request):
    auth_logout(request)
    messages.success(request, "Pomyślnie wylogowano.")
    return redirect('edziekanat_app:home')


def administrators(request):
    users = User.objects.all()
    edit_form = EditUserForm()
    return render(request, 'admin/administrators.html', context={'users': users, 'form': edit_form})


class UserCreator(SessionWizardView):
    template_name = "auth/register.html"

    def get_form_kwargs(self, step=None):
        kwargs = {}
        if step == '1':
            role = self.get_cleaned_data_for_step('0')['role']
            kwargs.update({'role': role, })
        return kwargs

    def done(self, form_list, **kwargs):
        email = self.get_cleaned_data_for_step('0')['email']
        password = self.get_cleaned_data_for_step('0')['password']
        password_repeat = self.get_cleaned_data_for_step('0')['password_repeat']
        role = self.get_cleaned_data_for_step('0')['role']
        first_name = self.get_cleaned_data_for_step('0')['first_name']
        last_name = self.get_cleaned_data_for_step('0')['last_name']
        address = self.get_cleaned_data_for_step('1')['address']
        phone = self.get_cleaned_data_for_step('1')['phone']
        birth_date = self.get_cleaned_data_for_step('1')['birth_date']
        allow_email_send = self.get_cleaned_data_for_step('1')['allow_email_send']

        if User.objects.filter(email=email).exists():
            messages.error(self.request, 'Użytkownik o takim adresie e-mail już istnieje.')
            return redirect('edziekanat_app:user_register')
        elif password != password_repeat:
            messages.error(self.request, 'Hasła nie zgadzają się.')
            return redirect('edziekanat_app:user_register')
        else:
            extra = {}
            if role.name == Student.base_role:
                extra = {
                    'course': self.get_cleaned_data_for_step('1')['course'],
                    'specialization': self.get_cleaned_data_for_step('1')['specialization'],
                }
            if role.name == Employee.base_role:
                extra = {
                    'job': self.get_cleaned_data_for_step('1')['job']
                }
            user = User.objects.create_user(
                password=password,
                email=email,
                role=role,
                phone=phone,
                address=address,
                birth_date=birth_date,
                allow_email_send=allow_email_send,
                extra=extra
            )
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            print(f"Zarejestrowano:\n"
                  f"Email:{user.email}\n"
                  f"Hasło:{user.password}\n"
                  f"Imie:{user.first_name}\n"
                  f"Nazwisko:{user.last_name}")
            login(self.request, user)
            messages.success(self.request, 'Pomyślnie zarejestrowano!')
        return redirect('edziekanat_app:home')
