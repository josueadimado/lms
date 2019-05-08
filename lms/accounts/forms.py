from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser,Employee,Leaves,LeaveType
from django.forms import DateInput
from django.utils import timezone
from django.db import models
from django.forms import ModelForm

def past_years(ago):
    this_year = timezone.now().year
    return list(range(this_year,this_year-ago-1))

class DateInput(DateInput):
    input_type='date'


class EmployeeCreationForm(UserCreationForm):
    # username = forms.CharField(max_length=200,
    # widget=(forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})))

    class Meta(UserCreationForm.Meta):
        model = Employee
        widgets = {'date_of_birth':DateInput()}
        fields = ('username','first_name','last_name','email','department','date_of_birth','gender','marital_status','city','country','country_code','phone','address')


class EmployeeChangeForm(UserChangeForm):
    class Meta:
        model = Employee
	#exclude = ['is_superuser']
        fields = ('username', 'email','password',)


class LeavesCreationForm(ModelForm):
    # username = forms.CharField(max_length=200,
    # widget=(forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})))

    class Meta:
        model = Leaves
        widgets = {'fromDate':DateInput(),'toDate':DateInput()}
        fields = ('description','leavetype','fromDate','toDate')


class LeavesChangeForm(ModelForm):
    class Meta:
        model = Leaves
        widgets = {'fromDate':DateInput(),'toDate':DateInput()}
        fields = ('description', 'leavetype','fromDate','toDate')