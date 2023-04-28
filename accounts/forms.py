from django import forms
from . models import Account


class RegistrationForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'create password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'confim password'}))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name',  'dob', 'email', 'phone_number', 'password']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter your first_name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter your last_name'
        self.fields['dob'].widget.attrs['placeholder'] = 'Example 2020-12-08'
        self.fields['email'].widget.attrs['placeholder'] = 'example@mail.com'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'enter your phone_number'

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('password and confirm_password does not match!')
