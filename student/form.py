from django import forms
from .models import students
from .models import Attendance, Marks

class student_form(forms.ModelForm):
    class Meta:
        model=students
        fields="__all__"


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields ="__all__"

class MarksForm(forms.ModelForm):
    class Meta:
        model = Marks
        fields ="__all__"

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if any(char.isdigit() for char in name):
            raise forms.ValidationError("Name should not contain numbers.")
        return name

    def clean_roll(self):
        roll = self.cleaned_data.get('roll')
        if not str(roll).isdigit():
            raise forms.ValidationError("Roll number must be numeric.")
        return roll