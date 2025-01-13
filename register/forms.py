# #Here we are going to import 2 things; the django form and the models we created cos we'd be using them
# from django import forms
# from . models import UserForm, SignIn, Transfer
# from django.core.exceptions import ValidationError
# from django.contrib.auth import authenticate
# from django.contrib.auth.hashers import make_password
# #create our django form by using the fields/attributes we listed in our models page


# class FormData(forms.ModelForm):
   
#     class Meta:
#         model = UserForm #Here, we just linked/mapped our model fields to this django inbuilt form
#         fields = ["firstname", "lastname", "username", "email", "password", "phonenumber"]

#     # def email(self):
#     #     email = UserForm.objects.get('email')
#     #     if UserForm.objects.filter(email=email).exists():
#     #         raise forms.ValidationError("This email is already registered")
#     #     return email.save()
    
# class SignInData(forms.ModelForm):

#     class Meta:
#         model = SignIn
#         fields = ["username", "password"]

# from django import forms
# from django.core.exceptions import ValidationError
# from django.contrib.auth.hashers import make_password
# from django.contrib.auth import authenticate
from .models import UserForm, SignIn, Transfer

# class FormData(forms.ModelForm):
#     password = forms.CharField(
#         widget=forms.PasswordInput(attrs={"placeholder": "Enter your password"}),
#         min_length=8,
#         help_text="Password must be at least 8 characters long."
#     )

#     class Meta:
#         model = UserForm
#         fields = ["firstname", "lastname", "username", "email", "password", "phonenumber"]

#     def clean_email(self):
#         email = self.cleaned_data.get("email")
#         if UserForm.objects.filter(email=email).exists():
#             raise ValidationError("This email is already registered.")
#         return email

#     def clean_password(self):
#         password = self.cleaned_data.get("password")
#         return make_password(password)  # Hash the password before saving

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password
from .models import UserForm

class FormData(forms.ModelForm):
    class Meta:
        model = UserForm  # Use the custom UserForm model
        fields = ['firstname', 'lastname', 'username', 'email', 'password', 'phonenumber']

    def clean_phonenumber(self):
        """Validate unique phone number."""
        phonenumber = self.cleaned_data['phonenumber']
        if UserForm.objects.filter(phonenumber=phonenumber).exists():
            raise forms.ValidationError("This phone number is already in use.")
        return phonenumber

    def clean_password(self):
        """Validate and hash password."""
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        return make_password(password)  # Hash password before saving


class SignInData(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)



class Transfer(forms.ModelForm):

    class Meta:
        model = Transfer
        fields = ["sender_name", "receiver_name", "amount"]



from django import forms
from .models import Deposit

class DepositForm(forms.ModelForm):
    class Meta:
        model = Deposit
        fields = ['amount']
