from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, UserUpdateForm
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash, get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.db import connection
from .models import Students, Courses, User, Prereqs, AuthUser, Section, Dep, Instructor, Timeslot
from django.template import loader

@login_required(login_url='home')
def addrecord(request,id,time):    

    user = User(course_ID=id, username = request.user, start_time = time)
    if User.objects.filter(course_ID=id, username = request.user).exists():
        messages.error(request, 'You have already taken this course')
    elif User.objects.filter(start_time=time, username = request.user).exists():
        messages.error(request, 'Time Clash')
    else:
        user.save()
    
    return HttpResponseRedirect(reverse('home'))

@login_required(login_url='home')
def offer(request,id):    

    name = request.POST['instructor_name']

    offer = Dep(section_id=id, username = request.user, instructor_name = name)

    offer.save()

    return HttpResponseRedirect(reverse('home'))

def offerform(request,id):

    q = "select section.section_ID, courses.course_ID, prereqs_ID, prereqs_names, credit_hours, courses.course_name from courses LEFT JOIN prereqs ON courses.course_ID = prereqs.course_ID LEFT JOIN section ON section.course_ID = courses.course_ID WHERE section.section_ID = " + str(id)

    query = Courses.objects.raw(q)
    
    return render(request, 'main/offerform.html',{'query': query})

def accept(request,sid,cid,iid):
    accept1 = Section.objects.get(section_id=sid)
    accept2 = Courses.objects.get(course_id=cid)

    username = str(request.user)
    
    name2 = "select id,first_name, last_name from auth_user where username = '" + username + "'"
    ans = AuthUser.objects.raw(name2)
    for p in ans:
        prof_name = "Proffessor " + str(p.first_name) + " " + str(p.last_name)

    user = Dep.objects.get(instructor_name = prof_name, section_id = sid)
    name = user.instructor_name
    i_id = Instructor.objects.get(instructor_name = name)
    newid = i_id.instructor_id

    accept1.instructor_id = newid
    accept2.instructor_id = newid



    accept1.save()
    accept2.save()

    return HttpResponseRedirect(reverse('home'))


def delete(request, id):
    record = User.objects.get(id=id)
    record.delete()
    return HttpResponseRedirect(reverse('home'))

def register(response):
    if response.method == "POST" :
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            messages.success(response, "You have created an account")
        redirect('home/')
    else:
        form = RegisterForm()

    return render(response, "main/register.html", {"form":form})

@login_required(login_url='login')
def home(request):
    username = str(request.user)

    name = "select id, first_name, last_name from auth_user WHERE username = '" + username + "'"
    names = AuthUser.objects.get(username=username)
    f = names.first_name

    cursor = connection.cursor()
    cursor.execute("select student_name from students")
    # cursor.close()
    query1 = cursor.fetchall()
    cursor = connection.cursor()
    cursor.execute("select instructor_name from instructor")
    # cursor.close()
    query2 = cursor.fetchall()
    #student instructor name check
    newq = []
    newq2 = []
    for x in query1:
        newq.append(x[0].split(" ")[0]);
    for x in query2:
        newq2.append(x[0].split(" ")[1]);
    
    counter_student = 0 
    counter_proffessor = 0
    for i in newq:
        if (f==str(i)):
            counter_student += 1
    for i in newq2:
        if (f==str(i)):
            counter_proffessor += 1
    if counter_student>0:
        boolean = 'student'
    if counter_proffessor>0:
        boolean = 'proff'
    else:
        boolean = 'none'

    q = "select id,section.section_ID, course_name, timeslot.start_time, timeslot.end_time, section_name from section INNER JOIN main_user ON section.section_ID = main_user.course_id INNER JOIN courses ON section.course_ID = courses.course_ID INNER JOIN timeslot ON timeslot.section_ID = section.section_ID WHERE main_user.username = '"+username+"'"

    q2 = Section.objects.raw(q)

    name2 = "select id,first_name, last_name from auth_user where username = '" + username + "'"
    ans = AuthUser.objects.raw(name2)
    for p in ans:
        prof_name = "Proffessor " + str(p.first_name) + " " + str(p.last_name)

    query3 = "select id, courses.instructor_id, Dep.section_ID, section_name, Dep.section_ID, department_name, courses.course_ID, prereqs_ID, prereqs_names, credit_hours, courses.course_name, start_time, end_time, instructor_name from Dep INNER JOIN section ON section.section_ID = Dep.section_ID INNER JOIN courses ON courses.course_ID = section.course_ID INNER JOIN prereqs ON courses.course_ID = prereqs.course_ID INNER JOIN timeslot ON timeslot.section_ID = section.section_ID WHERE instructor_name ='" + prof_name + "'"

    q3 = Dep.objects.raw(query3)

    query = Students.objects.raw("select student_ID, student_name from students")

    return render(request, 'main/home.html',{'query': query, 'q2': q2, 'bool':boolean, 'q3':q3})

def courses(request):
    if request.method == "POST":
        searched = request.POST['searched']

        q= "select section.section_ID, section.instructor_id, courses.course_ID, timeslot_ID, section.section_ID, course_name, instructor_name, department_name, credit_hours, courses.semester, start_time, end_time, classroom.classroom_ID, building_name, classroom.room_number, section_name from section LEFT JOIN instructor on instructor.instructor_ID = section.instructor_ID LEFT JOIN courses ON courses.course_ID = section.course_ID LEFT JOIN timeslot ON timeslot.section_ID = section.section_ID LEFT JOIN classroom ON classroom.room_number = section.room_number where course_name LIKE'%"+searched+"%' OR instructor_name LIKE '%"+searched+"%' OR department_name LIKE '%"+searched+"%' OR credit_hours LIKE '%"+searched+"%'"
        
        query = Courses.objects.raw(q)
        
        info = AuthUser.objects.get(username=request.user)


        return render(request, 'main/courses.html', {'searched':searched,'Courses':query, 'Dep': info})
    else:
        return render(request, 'main/course.html', {})


def profile(request, username):
    cursor = connection.cursor()
    q = ("select course_name, credit_hours, prereqs_names from courses INNER JOIN prereqs ON prereqs.course_ID = courses.course_ID")
    # cursor.close()
    query = Courses.objects.raw(q)

    if request.method == 'POST':
        user = request.user
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user_form = form.save()

            messages.success(request, f'{user_form}, Your profile has been updated!')
            return redirect('profile', user_form.username)

        for error in list(form.errors.values()):
            messages.error(request, error)
    user = get_user_model().objects.filter(username=username).first()

    if user:
        form = UserUpdateForm(instance=user)
        form.fields['username'].widget.attrs = {'rows': 1}
        return render(request, 'main/profile.html', context={'form': form, 'query':query})

    return redirect("homepage")



def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("/login")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="main/login.html", context={"login_form":form})

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.info(request, f"You have successfuly changed password.")
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'main/change_password.html', {'form': form})

def update(request, id):

    name = "select id,first_name, last_name from auth_user where id = " + str(id)
    ans = AuthUser.objects.raw(name)
    for p in ans:
        prof_name = "Proffessor " + str(p.first_name) + " " + str(p.last_name)

    q = "select courses.course_ID, prereqs_ID, prereqs_names, instructor_name, credit_hours from courses LEFT JOIN prereqs ON courses.course_ID = prereqs.course_ID LEFT JOIN instructor ON courses.instructor_id = instructor.instructor_ID WHERE instructor_name = '"+prof_name+"'"

    x = AuthUser.objects.get(username=request.user)
    query = Courses.objects.raw(q)
    y= int(str(x).split(" ")[2][1:-1])
    # template = loader.get_template('main/update.html')
    # context = {'course': query}
    # return HttpResponse(template.render(context, request))
    return render(request, 'main/update.html',{'course': query, 'id': y})

def updateform(request,cid,id):

    name = "select id,first_name, last_name from auth_user where id = " + str(id)
    ans = AuthUser.objects.raw(name)
    for p in ans:
        prof_name = "Proffessor " + str(p.first_name) + " " + str(p.last_name)

    q = "select courses.course_ID, prereqs_ID, prereqs_names, instructor_name, credit_hours, courses.course_name from courses LEFT JOIN prereqs ON courses.course_ID = prereqs.course_ID LEFT JOIN instructor ON courses.instructor_id = instructor.instructor_ID WHERE instructor_name = '"+prof_name+"' AND courses.course_id = " + str(id)

    query = Courses.objects.raw(q)

    ch = Courses.objects.get(course_id=cid)
    ci = Courses.objects.get(course_id=cid)
    pr = Prereqs.objects.get(course_id=cid)
    
    return render(request, 'main/updateform.html',{'query': query, 'ch': ch, 'pr': pr, 'ci' : ci})


def updaterecord(request,eid,id):
    credit = request.POST['credit_hours']
    prereq = request.POST['prereq']
    info = request.POST['course_info']
    ch = Courses.objects.get(course_id=id)
    ci = Courses.objects.get(course_id=id)
    pr = Prereqs.objects.get(course_id=id)
    ch.credit_hours = credit
    pr.prereqs_names = prereq
    ci.course_info = info
    ch.save()
    pr.save()
    ci.save()

    # messages.info(request, pr.prereqs_names)
    return HttpResponseRedirect(reverse('home'))



#-------------------------------------------------------------------------------------

def edit(request,id):

    q = "select timeslot_id, start_time, end_time, section_id, course_id, classroom_id from timeslot where section_id = " + str(id)

    query = Courses.objects.raw(q)
    
    return render(request, 'main/editform.html',{'query': query, 'id': id})


def editrecord(request,id):
    start = request.POST['start_time']
    end = request.POST['end_time']
    t = Timeslot.objects.get(section_id=id)
    t.start_time = start
    t.end_time = end
    t.save()

    return HttpResponseRedirect(reverse('home'))

def editstudent(request):

    name = "select id,first_name, last_name from auth_user where username = '" + str(request.user) + "'"
    ans = AuthUser.objects.raw(name)
    for p in ans:
        name = str(p.first_name)

    q = "select department.department_id, student_name, student_id, department_name, major, batch_year, total_credithours from students INNER JOIN department ON students.department_id = department.department_id WHERE department_name ='"+name+"'"

    query = Students.objects.raw(q)
    
    return render(request, 'main/editstudent.html',{'query': query})

def editstudentform(request,id):

    q = "select student_name, student_id, major, batch_year, total_credithours from students where student_id ="+str(id)

    query = Students.objects.raw(q)

    return render(request, 'main/editstudentform.html',{'id': id, 'student':query})

def editstu(request,id):

    # major = request.POST.get('is_private')
    total_credithours = request.POST['total_credithours']
    batch_year = request.POST['batch_year']
    t = Students.objects.get(student_id=id)
    # t.major = major
    t.total_credithours = total_credithours
    t.batch_year = batch_year
    t.save()

    return HttpResponseRedirect(reverse('home'))
