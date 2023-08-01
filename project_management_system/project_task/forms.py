from django import forms
from .models import Task,Employee,Group



class EmployeeRegistrationForm(forms.ModelForm):
    profile_image = forms.ImageField(label='Profile Image', required=False)

    class Meta:
        model = Employee
        fields = ['profile_image','name', 'email', 'username', 'password', 'role','phone_number','domain','technologies_used']


class EmployeeProfileForm(forms.ModelForm):
    
    class Meta:
        model = Employee
        fields = ['profile_image','name', 'email', 'username','password','role','phone_number','domain','technologies_used']



class GroupForm(forms.ModelForm):
    developers = forms.ModelMultipleChoiceField(
        queryset=Employee.objects.filter(role='Project Developer'),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Group
        fields = ['name', 'developers']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['developers'].queryset = Employee.objects.filter(role='Project Developer')


class TaskForm(forms.ModelForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=False)
    
    class Meta:
        model = Task
        fields = ['group', 'title', 'description', 'due_date', 'priority', 'status', 'assigned_to']


       