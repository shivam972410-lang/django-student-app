from django import forms
from .models import Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email', 'course', 'age']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'e.g. Asha Patel', 'autocomplete': 'name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'name@example.com', 'autocomplete': 'email'}),
            'course': forms.TextInput(attrs={'placeholder': 'e.g. Computer Science'}),
            'age': forms.NumberInput(attrs={'min': 1, 'max': 120}),
        }
