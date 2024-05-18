from django import forms
from .models import Student ,Course


class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Student
        fields = ['username', 'email', 'password', 'confirm_password']

    def clean_username(self):
        username = self.cleaned_data['username']
        if not username.replace(' ', '').isalpha():
            raise forms.ValidationError("Username only contain letters ")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        return password

    def clean_confirm_password(self):
        confirm_password = self.cleaned_data['confirm_password']
        if confirm_password != self.cleaned_data['password']:
            raise forms.ValidationError("Passwords do not match")
        return confirm_password

    def clean_email(self):
        email = self.cleaned_data['email']
        if Student.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100)  # Change to EmailField
    password = forms.CharField(widget=forms.PasswordInput())
    

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        return cleaned_data
    
from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_code', 'course_name', 'description', 'prerequisites']


from django import forms

class AddToRegistrationForm(forms.Form):
    selected_courses = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        course_choices = kwargs.pop('course_choices')
        super(AddToRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['selected_courses'].queryset = course_choices
