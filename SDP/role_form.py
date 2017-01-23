from django.contrib.auth.forms import AuthenticationForm
from django import forms


class DesignateForm(forms.Form):
    username = forms.CharField(label="AB ID", max_length=8,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))


class ControlAccessForm(forms.Form):
    username = forms.CharField(label="AB ID", max_length=8,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    is_active = forms.BooleanField(required=False, label="Allow to access SDP")


class RecordForm(forms.Form):
    username = forms.CharField(label="AB ID", max_length=8,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))


class AddCategoryForm(forms.Form):
    catname = forms.CharField(label='Category Title', max_length=127)
