from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Application

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already registered. Please use a different email.')
        return email

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['title', 'description', 'amount_requested', 'document']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'amount_requested': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'document': forms.FileInput(attrs={'class': 'form-control'}),
        }
    
    def clean_document(self):
        document = self.cleaned_data.get('document')
        if document:
            # Check file extension
            if not document.name.endswith(('.pdf', '.docx')):
                raise forms.ValidationError("Only PDF and DOCX files are allowed.")
            
            # Check file size (5MB max)
            if document.size > 5 * 1024 * 1024:  # 5MB in bytes
                raise forms.ValidationError("File size must be under 5MB.")
                
        return document