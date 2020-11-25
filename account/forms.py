from django import forms
from django.contrib.auth.forms import UserChangeForm,UserCreationForm
from .models import MyUser,Category


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=False)
    image = forms.ImageField(required=False)
    phone = forms.CharField(required=False,help_text=("With country code"))
            
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = "Password must contain at least 8 characters."
        self.fields['password2'].label = "Password confirm"
        self.fields['username'].help_text = " Letters, digits and @/./+/-/_ only."               

    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name','username','email','phone','password1', 'password2']


class UserUpdateForm(UserChangeForm):
    email = forms.EmailField(required=False)
    image = forms.ImageField(required=False)
    phone = forms.CharField(required=False,help_text=("With country code"))

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = " Letters, digits and @/./+/-/_ only."
        self.fields['image'].label = ""

    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name','username','email','phone','image']

