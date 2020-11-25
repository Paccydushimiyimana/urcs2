import json
from django.shortcuts import render, redirect, get_object_or_404 
from .models import College,School,Department,Category,Student_category,Lecturer_category
from .models import Department_council,School_council,College_council,Academic_council,MyUser
from announce.models import Announce
from chat.models import Chat_room as Room
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm,AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMessage
from django.utils.translation import ugettext as _
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from account.forms import SignUpForm,UserUpdateForm
from django.views.decorators.csrf import csrf_exempt
from twilio.rest import Client
from django.http import HttpResponse


def signup_view(request):
    login_form=AuthenticationForm()
    signup_form=SignUpForm()
    _form = request.POST.get('form_name')
    if _form == 'login_form':
    # Loging in user
        login_form=AuthenticationForm(request,request.POST)
        if login_form.is_valid():
            username=login_form.cleaned_data.get('username')
            password=login_form.cleaned_data.get('password')
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'User {user} is logged in .')           
                return redirect('home')
        else:
            messages.warning(request, f'Invalid credentials!...Correct the errors on the form')
    if _form == 'signup_form':  
    # Signing up user          
        signup_form=SignUpForm(request.POST,request.FILES)
        if signup_form.is_valid():
            user=signup_form.save()
            user.category=request.POST.get('Catgy')
            user.student=request.POST.get('Std_cat')
            user.regNo=request.POST.get('Reg')
            user.lecturer=request.POST.get('Lect_cat')
            user.staffId=request.POST.get('Staff')
            user.college_council=request.POST.get('Col_council_cat')
            user.academic_council=request.POST.get('Acad_council_cat')
            user.school_council=request.POST.get('Skl_council_cat')
            user.department_council=request.POST.get('Dep_council_cat')
            user.school=request.POST.get('Skl')
            user.department=request.POST.get('Depart')
            user.level=request.POST.get('Lv')
            user.save()
            username = signup_form.cleaned_data.get('username')
            password = signup_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user) 
            messages.success(request, f'Account created succesfully for {username}')
            return redirect('home')
        else:
            messages.warning(request, f'User not created!...Correct the errors on the form')

    context={'categories':Category.objects.all(),'signup_form':signup_form,'login_form':login_form}
    return render(request,'signup.html',context)

@login_required
def profile_view(request,name):
    user = request.user
    board_announces=Announce.objects.all().filter(sender= user) 
    inbox_announces=[]
    chat_rooms = []
    for announcet in Announce.objects.all():
        if user in announcet.receiver.all() and announcet.general==False:
            inbox_announces.append(announcet)
    for room in Room.objects.all():
        if user == room.me or user == room.other:  
            chat_rooms.append(room)

    update_form=UserUpdateForm(instance=user)
    pwd_form = PasswordChangeForm(request.user)

    _form = request.POST.get('form_name')
    if _form == 'logout_form':
    # Logging out user
        user = request.user
        logout(request)
        messages.success(request, f'User {user} is logged out')
        return redirect('home')
    if _form == 'update_form':  
    # Updating user          
        update_form=UserUpdateForm(request.POST,request.FILES,instance=user)
        if update_form.is_valid():
            user=update_form.save()
            user.category=request.POST.get('Catgy')
            user.student=request.POST.get('Std_cat')
            user.regNo=request.POST.get('Reg')
            user.lecturer=request.POST.get('Lect_cat')
            user.staffId=request.POST.get('Staff')
            user.college_council=request.POST.get('Col_council_cat')
            user.academic_council=request.POST.get('Acad_council_cat')
            user.school_council=request.POST.get('Skl_council_cat')
            user.department_council=request.POST.get('Dep_council_cat')
            user.school=request.POST.get('Skl')
            user.department=request.POST.get('Depart')
            user.level=request.POST.get('Lv')
            user.save()
            messages.success(request, f'Account updated succesfully for {user} ')
            return redirect('home')
        else:
            messages.warning(request, f'Account not updated!...Correct the errors on the form')
    if _form == 'pwd_form':
    # Changing password  
        pwd_form = PasswordChangeForm(request.user, request.POST) 
        if pwd_form.is_valid():
            user = pwd_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, f'Your password was . updated!')
            return redirect('change_password')
        else:
            messages.warning(request, f'Please correct the error!...')
    context={
        'inbox':len(inbox_announces),'board':len(board_announces),
        'chats':len(chat_rooms),'categories':Category.objects.all(),
        'update_form':update_form,'pwd_form':pwd_form,'user':user,
        'profile':1,'cat':user.category
        }

    student_cats=Student_category.objects.all()
    lecturer_cats=Lecturer_category.objects.all()
    col_council_cats=College_council.objects.all()
    skl_council_cats=School_council.objects.all()
    dep_council_cats=Department_council.objects.all()
    acad_council_cats=Academic_council.objects.all()
    schools=School.objects.all()    
    ctx2 = {
        'student_cats':student_cats,'lecturer_cats':lecturer_cats,
        'col_council_cats':col_council_cats,'dep_council_cats':dep_council_cats,
        'skl_council_cats':skl_council_cats,'acad_council_cats':acad_council_cats,'schools':schools
        }
    context.update(ctx2)
    return render(request,'profile.html',context)

def load_category(request):
    cat=request.GET.get('category')
    page = request.GET.get('page')
    # print(current)
    student_cats=Student_category.objects.all()
    lecturer_cats=Lecturer_category.objects.all()
    col_council_cats=College_council.objects.all()
    skl_council_cats=School_council.objects.all()
    dep_council_cats=Department_council.objects.all()
    acad_council_cats=Academic_council.objects.all()
    schools=School.objects.all()
    context={'cat':cat,'student_cats':student_cats,'lecturer_cats':lecturer_cats,'col_council_cats':col_council_cats,
            'dep_council_cats':dep_council_cats,'skl_council_cats':skl_council_cats,'acad_council_cats':acad_council_cats,
            'page':page,'schools':schools}
    return render(request, 'category.html', context)

def load_departments(request):
    j_skl= request.GET.get('school')
    page = request.GET.get('page')
    # print(str(j_skl))
    skls = json.loads(j_skl)
    departments=[]
    if page == 'create':
        schools=[]
        for skl in skls:
            school = School.objects.get(name=skl)
            schools.append(school)
        for school in schools:
            departs = school.departments.all()
            for depart in departs:
                departments.append(depart)
        context={'departments':departments,'page':page}       

    else:
        school = School.objects.get(name=skls)
        departments=  school.departments.all()       
        context={'departments':departments}
    return render(request, 'options/dep_options.html', context)

def load_levels(request):
    j_depart=request.GET.get('department')
    page = request.GET.get('page')
    departs = json.loads(j_depart)
    if page == 'create':
        departments=[]
        _department = []
        _max = 0

        for depart in departs:
            department = Department.objects.get(name=depart)
            departments.append(department)
        for department in departments:
            lvls = department.levels
            if lvls > _max:
                _max = lvls
                levels=[]
                for lvl in range(lvls+1):
                    if lvl>0:
                        level='Lv '+str(lvl)
                        levels.append(level)
        context={'levels':levels,'page':page}
    else:
        department=Department.objects.get(name=departs)
        lvls=department.levels 
        levels=[]
        for lvl in range(lvls+1):
            if lvl>0:
                level='Lv '+str(lvl)
                levels.append(level)
        context={'levels':levels}
    return render(request, 'options/lv_options.html', context)
 
def sms(request):
    user=request.user
    ann=Announce.objects.last()
    context={'user':user,'ann':ann}
    tolst =['+250727462915','+250782644566','+250784017638','+250785011856','+250728915557']
    message=render_to_string('mail.html',context)
    body = strip_tags(message)
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    for to in tolst:
        response = client.messages.create(body=body,to=to,from_=settings.TWILIO_PHONE_NUMBER) 
    return HttpResponse('Okay')  

def login_view(request):
    login_form=AuthenticationForm(request,request.POST or None)
    if login_form.is_valid():
        username=login_form.cleaned_data.get('username')
        password=login_form.cleaned_data.get('password')
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'User {user} is logged in .')           
            return redirect(request.GET.get('next'))
            # return redirect('home')
    context={'login_form':login_form}        
    return render(request,'login.html',context)