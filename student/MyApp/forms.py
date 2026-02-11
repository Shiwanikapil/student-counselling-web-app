from django import forms
from .models import StudentCounselling

class StudentCounsellingForm(forms.ModelForm):
    class Meta:
        model = StudentCounselling
        fields = '__all__'
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 2}),
            'pref1': forms.Select(choices=[
                ('Computer Science', 'Computer Science'),
                ('Electronics', 'Electronics'),
                ('Mechanical', 'Mechanical'),
                ('Civil', 'Civil'),
            ]),
            'pref2': forms.Select(choices=[
                ('Computer Science', 'Computer Science'),
                ('Electronics', 'Electronics'),
                ('Mechanical', 'Mechanical'),
                ('Civil', 'Civil'),
            ]),
        }
