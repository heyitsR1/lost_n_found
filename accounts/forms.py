from django import forms
from django.contrib.auth.forms import UserCreationForm
from allauth.account.forms import SignupForm
from .models import CustomUser

class CustomSignupForm(SignupForm):
    student_id = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-secondary focus:border-secondary',
            'placeholder': 'Enter your student ID (e.g., K123456)'
        }),
        help_text='Enter your university student ID (e.g., K123456)'
    )
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-secondary focus:border-secondary',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-secondary focus:border-secondary',
            'placeholder': 'Last Name'
        })
    )
    phone_number = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-secondary focus:border-secondary',
            'placeholder': 'Phone Number (optional)'
        })
    )
    department = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-secondary focus:border-secondary',
            'placeholder': 'Department (optional)'
        })
    )
    graduation_year = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-secondary focus:border-secondary',
            'placeholder': 'Graduation Year (optional)',
            'min': '2020',
            'max': '2030'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Update password fields with correct CSS classes
        self.fields['password1'].widget.attrs.update({
            'class': 'block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-secondary focus:border-secondary',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-secondary focus:border-secondary',
            'placeholder': 'Confirm Password'
        })
        # Update email field with correct CSS classes
        self.fields['email'].widget.attrs.update({
            'class': 'block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-secondary focus:border-secondary',
            'placeholder': 'Email address'
        })

    def save(self, request):
        user = super().save(request)
        user.student_id = self.cleaned_data['student_id']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data.get('phone_number', '')
        user.department = self.cleaned_data.get('department', '')
        user.graduation_year = self.cleaned_data.get('graduation_year')
        user.save()
        return user

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'student_id', 'first_name', 'last_name', 'phone_number', 'department', 'graduation_year')