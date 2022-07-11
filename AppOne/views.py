from django.shortcuts import render
from AppOne.forms import *
from AppOne.models import StudentClassModel, UserClassExtension

from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def start_page_parent(request):
    user = request.user
    username = user.username
    extension = UserClassExtension.objects.get(User = user)
    extension = extension.class_id.full_class_name
    group = []
    for gr in request.user.groups.all():
        group.append(gr.name)

    return render(request, "AppOne/start_page_parent.html", {'username' : username, 
                                                        'group' : group, 
                                                        'extension': extension } )


@login_required
def start_page_teacher(request):
    user = request.user
    username = user.username
    extension = UserClassExtension.objects.get(User = user)
    extension = extension.class_id.full_class_name
    group = []
    for gr in request.user.groups.all():
        group.append(gr.name)

    return render(request, "AppOne/start_page_teacher.html", {'username' : username, 
                                                        'group' : group, 
                                                        'extension': extension } )


@login_required
def edit_student_marks(request, pk):
    valid_grades = StudentMarksModel.Marks.values
    tasks = TaskModel.objects.values

    if request.method == 'POST':
        form_grade = request.POST.get('grade')
        form_task = request.POST.get('task')
        get_task = TaskModel.objects.get(pk= form_task)
        
        new_grade = StudentMarksModel.objects.get(pk = pk)
        new_grade.mark = form_grade
        new_grade.task = get_task

        new_grade.save()

        print("[UPDATED FORM]")
        return HttpResponseRedirect(reverse("AppOne:edit_student_marks", args = [pk]))    

    grade = StudentMarksModel.objects.get(pk = pk)
    print(f"[OCENA]: {grade.mark}")
    
    return render(request, "AppOne/edit_student_marks.html", {'grade' : grade,
                                                         'valid_grades' : valid_grades,
                                                         'tasks' : tasks, })


@login_required
def student_marks(request, pk):
    print(f"[STUDENT ID]: {pk}" )
    student = StudentProfileModel.objects.get(pk = pk)
    marks = StudentMarksModel.objects.filter(student_id=student)
    valid_grades = StudentMarksModel.Marks.values
    tasks = TaskModel.objects.values
    
    if request.method == 'POST':
        form_grade = request.POST.get('grade')
        form_task = request.POST.get('task')
        get_task = TaskModel.objects.get(pk= form_task)
        
        new_grade = StudentMarksModel()
        new_grade.mark = form_grade
        new_grade.student_id = student
        new_grade.task = get_task

        new_grade.save()

        print("[SENDED FORM]")
        return HttpResponseRedirect(reverse("AppOne:student_marks", args = [pk]))

    return render(request, "AppOne/student_marks.html", {'student' : student,
                                                         'marks': marks,
                                                         'valid_grades' : valid_grades,
                                                         'tasks' : tasks, })


@login_required
def child_grades(request):
    username = request.user.username
    parent = User.objects.get(username = username)
    student = StudentProfileModel.objects.get(parent = parent)
    grades = StudentMarksModel.objects.filter(student_id = student)
    return render(request, 'AppOne/child_grades.html', {'grades' : grades,
                                                        'student': student})

@login_required
def child_managment(request):
    message = "START"
    username = request.user.username
    user = User.objects.get(username=username)
    if StudentProfileModel.objects.filter(parent=user).exists():
        child_model = StudentProfileModel.objects.get(parent=user)
        if request.method == 'POST':
            button = request.POST.get('submit')
            if button == "DELETE":
                child_model.delete()
                return render(request, "AppOne/child_managment.html", {'message' : message,
                                                                  'form_mode': True})
        return render(request, "AppOne/child_managment.html", {'message' : message,
                                                               'form_mode': False,
                                                               'child_model' : child_model })
    else:
        if request.method == 'POST':
            button = request.POST.get('submit')
            if button != "DELETE":
                student_form = StudentProfileModel()
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')

                if len(first_name) == 0 or len(last_name) == 0:
                    message = "NAME OR SURNAME CAN'T BE EMPTY"
                    return render(request, "AppOne/child_managment.html", {'message' : message,
                                                                            'form_mode': True})

                student_form.first_name = first_name
                student_form.last_name = last_name

                student_form.parent = user

                class_id = UserClassExtension.objects.get(User = user)
                class_id = class_id.class_id

                student_form.class_id = class_id
        
                student_form.save()
                child_model = StudentProfileModel.objects.get(parent=user)
                return render(request, "AppOne/child_managment.html", {'form_mode': False,
                                                               'child_model' : child_model })

        else: 
            message = "NOT POST"
        
        return render(request, "AppOne/child_managment.html", {'message' : message,
                                                               'form_mode': True})


@login_required
def list_of_students(request):
    user = request.user
    extension = UserClassExtension.objects.get(User = user)
    extension = extension.class_id
    students = StudentProfileModel.objects.filter(class_id = extension )
    return render(request, "AppOne/list_of_students.html", {'students' : students} )


@login_required
def raport(request):
    counter = {}
    averages_list = {}

    tasks = TaskModel.objects.filter()
    grades = StudentMarksModel.objects.filter()
    for task in tasks:
        counter[task.pk] = 0
        sum = 0
        for grade in grades:
            if task == grade.task:
                counter[task.pk] += 1
                match grade.mark:
                    case 'A' : sum += 5
                    case 'B' : sum += 4.5
                    case 'C' : sum += 4
                    case 'D' : sum += 3.5
                    case 'E' : sum += 3
        if counter[task.pk] > 0:
            averages_list[task.pk] = sum/counter[task.pk]
        else:
            averages_list[task.pk] = 0
    print('[INFO]')
    print(counter)
    print(averages_list)
    return render(request, "AppOne/raport.html" , {'tasks' : tasks,
                                                   'counter' : counter,
                                                   'averages_list' : averages_list} ) 


@login_required
def task_managment(request):
    message = ''
    if request.method == 'POST':
        task_form = TaskForm(data=request.POST)
        if task_form.is_valid():
            task_form.save()
            return HttpResponseRedirect(reverse('AppOne:task_managment'))
        else:
            message = "Błędny formularz"
    
    task_form = TaskForm()
    existing_forms = TaskModel.objects.filter()
    return render(request, "AppOne/task_managment.html", {'task_form' : task_form,
                                                          'existing_forms' : existing_forms,
                                                          'message' : message} )


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password = password)

        if user:
            if user.is_active:
                login(request, user)
                actual_user = User.objects.get(username = username)
                group = actual_user.groups.all()
                group = group[0]
                group = str(group)
                print(f"[GROUP]: {group}")
                if group == "Teacher":
                    return redirect('AppOne:start_page_teacher')
                else:
                    return redirect('AppOne:start_page_parent')
            else:
                return HttpResponseRedirect(reverse(''))
        else:
            print("Someone failed to login")
            print(f"Username: {username} and password {password}")
            return render(request, "AppOne/login.html", {'error' : True})

    return render(request, "AppOne/login.html", {'error' : False} )


def register(request):

    registered = False
    error_value = False
    if request.method == "POST":
        form_username = request.POST.get('email')
        form_first_name = request.POST.get('first_name')
        form_last_name = request.POST.get('last_name')
        form_email = form_username
        form_password = request.POST.get('password')
        form_repeat_password = request.POST.get('repeat_password')
        form_class_id = request.POST.get('class_id')
        form_group = request.POST.get('groups')
        error_value = False
        if User.objects.filter(username=form_username).exists():  
            error_value = "User already exist"  
        elif len(form_username) == 0:
            error_value = "Enter email"
        elif form_username.find("@") == -1:
            error_value = "Email must contain '@' sign" 
        elif len(form_password) == 0:
            error_value = "Enter password " 
        elif form_password != form_repeat_password:
            error_value = "Those passwords didn’t match. Try again."   
        elif len(form_first_name) == 0:
            error_value = "Enter your first name" 
        elif len(form_last_name) == 0:
            error_value = "Enter your last name" 
        else:
            user = User.objects.create_user(username = form_username,
                        first_name = form_first_name,
                        last_name = form_last_name,
                        email = form_email)
            user.set_password(form_password)
            if user.is_active:
                user.save()
                registered = True
                my_group = Group.objects.get(name=form_group)
                my_group.user_set.add(user)

                class_id_ins = StudentClassModel.objects.get(class_id = form_class_id)
                user_extension = UserClassExtension(User=user, class_id = class_id_ins)
                user_extension.save()

                error_value = "Registered"
            else:
                print(user.errors)

    user_form = RegistrationForm()
    user_extension_form = RegistrationExtensionForm()
    student_class = StudentClassModel.objects.all()
    group_model = Group.objects.all()

    return render(request, "AppOne/registration.html",
                {'user_form' : user_form,
                'user_extension_form' : user_extension_form,
                'student_class' : student_class,
                'group_model' : group_model,
                'registered' : registered,
                'error_value' : error_value})


def logout_user(request):
    logout(request)
    return render(request,"AppOne/logout_page.html")

