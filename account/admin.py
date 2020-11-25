from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import SignUpForm,UserUpdateForm
from .models import *

class MyUserAdmin(UserAdmin):
    add_form = SignUpForm
    form = UserUpdateForm
    model = MyUser
    list_display = ['username','email','first_name']

admin.site.register(MyUser,MyUserAdmin)
admin.site.register(College)
admin.site.register(School)
admin.site.register(Department)
admin.site.register(Category)
admin.site.register(Student_category)  
admin.site.register(College_council)
admin.site.register(School_council)
admin.site.register(Department_council)  
admin.site.register(Academic_council)
admin.site.register(Lecturer_category)

