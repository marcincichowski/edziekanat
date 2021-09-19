from django import forms
from edziekanat_app.models.tables.invoice_category import InvoiceCategory
from edziekanat_app.models.tables.invoice import Invoice


class RegisterForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input is-medium', 'placeholder': 'Imię'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input is-medium', 'placeholder': 'Nazwisko'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'input is-medium', 'placeholder': 'Adres e-mail'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input is-medium', 'placeholder': 'Hasło'}))
    password_repeat = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input is-medium', 'placeholder': 'Powtórz hasło'}))


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'input is-medium', 'placeholder': 'Adres e-mail'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input is-medium', 'placeholder': 'Hasło'}))


class CategoryPickForm(forms.Form):
    category = forms.ModelChoiceField(queryset=InvoiceCategory.objects.all()) # , widget=forms.Select(attrs={'class': 'input'})


class InvoicePickForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.category = kwargs.pop('category')
        super(InvoicePickForm, self).__init__(*args, **kwargs)
        self.fields['invoice'].queryset = Invoice.objects.filter(category=self.category)

    class Meta:
        model = Invoice
        fields = ['invoice']

    invoice = forms.ChoiceField()


class AddDictionaryValueCathedral(forms.Form):
    value = forms.CharField(widget=forms.TextInput(attrs={'class': 'input is-primary is-fullwidth', 'placeholder': 'Nazwa katedry'}))

    def __init__(self, *args, **kwargs):
        super(AddDictionaryValueCathedral, self).__init__(*args, **kwargs)
        self.fields['value'].label = ""
