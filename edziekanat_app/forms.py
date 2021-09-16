from django import forms


class RegisterForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input is-medium', 'placeholder': 'Imię'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input is-medium', 'placeholder': 'Nazwisko'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'input is-medium', 'placeholder': 'Adres e-mail'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input is-medium', 'placeholder': 'Hasło'}))
    password_repeat = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input is-medium', 'placeholder': 'Powtórz hasło'}))


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'input is-medium', 'placeholder': 'Adres e-mail'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input is-medium', 'placeholder': 'Hasło'}))


class AddDictionaryValueCathedral(forms.Form):
    value = forms.CharField(widget=forms.TextInput(attrs={'class': 'input is-primary is-fullwidth', 'placeholder': 'Nazwa katedry'}))

    def __init__(self, *args, **kwargs):
        super(AddDictionaryValueCathedral, self).__init__(*args, **kwargs)
        self.fields['value'].label = ""