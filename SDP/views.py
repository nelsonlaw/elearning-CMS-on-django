import re

import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User, Permission
from django.db.models import F

from SDP.models import Category
from SDP.models import Course
from SDP.models import Module
from SDP.models import Component
from SDP.models import Enrollment
from SDP.models import Employee
from SDP.models import Administrators
from SDP.models import Instructor
from SDP.models import HR

from .create_course_form import CourseInfoForm, ModuleInfoForm, \
    TextComponentInfoForm, ImageComponentInfoForm, FileComponentInfoForm, VideoComponentInfoForm, QuizComponentInfoForm
from .login_form import RegisterForm
from .role_form import DesignateForm, ControlAccessForm, RecordForm, AddCategoryForm


def whoami(uid):
    return Employee.objects.filter(user_id__exact=uid)[0]


@login_required(login_url="/login/")
def home(request):
    me = whoami(request.user.id)
    enrollment_info = Enrollment.objects.filter(employee=me)
    if enrollment_info:
        taking_courses = []
        for enrollment in enrollment_info.filter(completed=False):
            taking_courses.append(enrollment.course)
        completed_courses = []
        for enrollment in enrollment_info.filter(completed=True):
            completed_courses.append((enrollment.course, enrollment.completed_date))
    else:
        taking_courses = []
        completed_courses = []
    return render(request, 'home.html', {'categories': Category.objects.all(),
                                         'whoami': me,
                                         'role': "participant",
                                         'taking_courses': taking_courses,
                                         'completed_courses': completed_courses})


@login_required(login_url="/login/")
@permission_required('SDP.instructor', login_url="/no_permission")
def home_instructor(request):
    me = whoami(request.user.id)
    teaching_info = Course.objects.filter(instructor=me)
    if teaching_info:
        teaching_courses = []
        for teaching in teaching_info:
            teaching_courses.append(teaching)
    else:
        teaching_courses = None
    return render(request, 'home_instructor.html', {'whoami': me,
                                                    'role': "instructor",
                                                    'teaching_courses': teaching_courses})


@login_required(login_url="/login/")
@permission_required('SDP.HR', login_url="/no_permission")
def home_hr(request):
    me = whoami(request.user.id)
    return render(request, 'home_hr.html', {'whoami': me,
                                            'role': "HR"})


@login_required(login_url="/login/")
@permission_required('SDP.admin', login_url="/no_permission")
def home_admin(request):
    me = whoami(request.user.id)
    return render(request, 'home_administrator.html', {'whoami': me,
                                                       'role': "administrator"})


@login_required(login_url="/login/")
@permission_required('SDP.admin', login_url="/no_permission")
def designate(request):
    me = whoami(request.user.id)
    if request.method == 'POST':
        form = DesignateForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            user = User.objects.filter(username=username)
            if not user:
                return HttpResponse("No such user.")
            employee = Employee.objects.filter(user=user[0])
            if Instructor.objects.filter(employee=employee[0]):
                return HttpResponse("User is already a instructor.")
            permission = Permission.objects.get(codename='instructor')
            user[0].user_permissions.add(permission)
            new_instructor = Instructor.objects.create(employee=employee[0])
            new_instructor.save()
            return redirect("/home_admin/")
    else:
        form = DesignateForm()
    return render(request, 'designate.html', {'whoami': me,
                                              'role': 'administrator',
                                              'form': form})


@login_required(login_url="/login/")
@permission_required('SDP.admin', login_url="/no_permission")
def control_access(request):
    me = whoami(request.user.id)
    if request.method == 'POST':
        form = ControlAccessForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            user = User.objects.filter(username=username)
            if not user:
                return HttpResponse("No such user.")

            if 'is_active' in request.POST:
                is_active = True
            else:
                is_active = False
            new_status = user.update(is_active=is_active)
            return redirect("/home_admin/")
    else:
        form = ControlAccessForm()
    return render(request, 'control_acces.html', {'whoami': me,
                                                  'role': 'administrator',
                                                  'form': form})


@login_required(login_url="/login/")
def category(request, cid):
    me = whoami(request.user.id)
    select_category = Category.objects.filter(category_id=cid)[0]
    course_in_category = Course.objects.filter(category__category_id=cid, open=True)
    return render(request, 'category.html', {'categories': Category.objects.all(),
                                             'whoami': me,
                                             'select_category': select_category,
                                             'role': 'participant',
                                             'course_in_category': course_in_category})


@login_required(login_url="/login/")
def course(request, course_id):
    course = Course.objects.filter(course_id=course_id)
    me = whoami(request.user.id)
    if course:
        if not Enrollment.objects.filter(employee=me, course=course[0]):
            return HttpResponse("You haven't enrolled in this course.")
        select_course = course[0]
        progress = Enrollment.objects.filter(course=select_course, employee=me)[0].progress
        total = Module.objects.filter(course=select_course).count()
        module_in_course = Module.objects.filter(course__course_id=course_id, order=progress)
        module_with_components = []
        for module in module_in_course:
            module_with_components.append(
                (module, Component.objects.filter(module__module_id=module.module_id).order_by('order')))
    else:
        HttpResponse("No such course")
    return render(request, 'course.html', {'categories': Category.objects.all(),
                                           'whoami': me,
                                           'role': 'participant',
                                           'select_course': select_course,
                                           'total': total,
                                           'module_with_components': module_with_components})


@login_required(login_url="/login/")
@permission_required('SDP.instructor', login_url="/no_permission")
def modify_course(request, course_id):
    me = whoami(request.user.id)
    course = Course.objects.filter(course_id=course_id)
    if course:
        select_course = course[0]
        if select_course.instructor != me:
            return HttpResponse("You are not allow to modify this course.")
        module_in_course = Module.objects.filter(course__course_id=course_id).order_by('order')
        module_with_components = []
        for module in module_in_course:
            module_with_components.append(
                (module, Component.objects.filter(module__module_id=module.module_id).order_by('order')))
    else:
        HttpResponse("No such course")
    return render(request, 'modify_course.html', {'categories': Category.objects.all(),
                                                  'whoami': me,
                                                  'select_course': select_course,
                                                  'role': 'instructor',
                                                  'module_with_components': module_with_components})


@login_required(login_url="/login/")
@permission_required('SDP.instructor', login_url="/no_permission")
def modify_course_order(request, course_id):
    me = whoami(request.user.id)
    course = Course.objects.filter(course_id=course_id)
    if course:
        if request.method == 'POST' and request.POST['change'] == "change":
            for key, pos in request.POST.items():
                if key.startswith("order_m"):
                    module_key = int(key[7:])
                    Module.objects.filter(module_id__exact=module_key).update(order=int(pos))
                if key.startswith("order_c"):
                    component_key = int(key[7:])
                    Component.objects.filter(component_id__exact=component_key).update(order=int(pos))
            return redirect("/modify_course/" + course_id)
        else:
            select_course = course[0]
            module_in_course = Module.objects.filter(course__course_id=course_id).order_by('order')
            module_with_components = []
            for module in module_in_course:
                module_with_components.append(
                    (module, Component.objects.filter(module__module_id=module.module_id).order_by('order')))
    else:
        HttpResponse("No such course")
    return render(request, 'modify_course_order.html', {'categories': Category.objects.all(),
                                                        'whoami': me,
                                                        'role': 'instructor',
                                                        'select_course': select_course,
                                                        'course_id': course_id,
                                                        'module_with_components': module_with_components})


@login_required(login_url="/login/")
@permission_required('SDP.instructor', login_url="/no_permission")
def create_module(request, course_id):
    me = whoami(request.user.id)
    course = Course.objects.filter(course_id__exact=int(course_id))
    if course:
        if request.method == 'POST':
            form = ModuleInfoForm(request.POST)
            if form.is_valid():
                title = request.POST['title']
                order = Module.objects.filter(course=course[0]).count() + 1
                new_module = Module.objects.create(title=title, course=course[0], order=order)
                new_module.save()
                return redirect("/modify_course/" + course_id)
        else:
            course_title = "Create a new module to " + course[0].title
            form = ModuleInfoForm()
    else:
        return HttpResponse("Error: Course not found")
    return render(request, 'create_module.html', {'categories': Category.objects.all(),
                                                  'whoami': me,
                                                  'role': 'instructor',
                                                  'form': form,
                                                  'course_id': course_id,
                                                  'course_title': course_title})


@login_required(login_url="/login/")
@permission_required('SDP.instructor', login_url="/no_permission")
def create_component(request, module_id, type):
    me = whoami(request.user.id)
    module = Module.objects.filter(module_id__exact=int(module_id))
    if module:
        course = module[0].course
        module_title = "Add a " + type + " to " + module[0].title
        if request.method == 'POST':
            if type == "text":
                form = TextComponentInfoForm(request.POST)
            elif type == "image":
                form = ImageComponentInfoForm(request.POST, request.FILES)
            elif type == "file":
                form = FileComponentInfoForm(request.POST, request.FILES)
            elif type == "video":
                form = VideoComponentInfoForm(request.POST)
            elif type == "quiz":
                form = QuizComponentInfoForm(request.POST)
            if form.is_valid():
                title = request.POST['title']
                order = Component.objects.filter(module=module[0]).count() + 1
                if type == "text":
                    content = request.POST['content']
                    new_component = Component.objects.create(module=module[0], title=title, order=order, type=type,
                                                             text_content=content)
                elif type == "image":
                    content = request.FILES['content']
                    new_component = Component.objects.create(module=module[0], title=title, order=order, type=type,
                                                             image_content=content)
                elif type == "file":
                    content = request.FILES['content']
                    new_component = Component.objects.create(module=module[0], title=title, order=order, type=type,
                                                             file_content=content)
                elif type == "video":
                    content = request.POST['content']
                    new_component = Component.objects.create(module=module[0], title=title, order=order, type=type,
                                                             video_url=content)
                elif type == "quiz":
                    question = request.POST['question']
                    answer = request.POST['answer']
                    new_component = Component.objects.create(module=module[0], title=title, order=order, type=type,
                                                             question=question, answer=answer)
                new_component.save()
                return redirect("/modify_course/" + str(course.course_id))
        else:
            if type == "text":
                form = TextComponentInfoForm()
            elif type == "image":
                form = ImageComponentInfoForm()
            elif type == "file":
                form = FileComponentInfoForm()
            elif type == "video":
                form = VideoComponentInfoForm()
            elif type == "quiz":
                form = QuizComponentInfoForm()
            else:
                return HttpResponse("Error: unknown component type")
    else:
        return HttpResponse("Error: module not found")
    return render(request, 'create_component.html', {'categories': Category.objects.all(),
                                                     'whoami': me,
                                                     'role': 'instructor',
                                                     'form': form,
                                                     'type': type,
                                                     'module_id': module_id,
                                                     'module_title': module_title})


@login_required(login_url="/login/")
@permission_required('SDP.instructor', login_url="/no_permission")
def create(request):
    me = whoami(request.user.id)
    if request.method == 'POST':
        form = CourseInfoForm(request.POST)
        if form.is_valid():
            title = request.POST['title']
            description = request.POST['description']
            category_id = request.POST['category']
            select_category = Category.objects.filter(category_id=int(category_id))[0]
            new_course = Course.objects.create(title=title, description=description,
                                               open=False, category=select_category,
                                               instructor=me)
            new_course.save()
            return redirect("/home_instructor/")
    else:
        form = CourseInfoForm()
    return render(request, 'create.html', {'categories': Category.objects.all(),
                                           'whoami': me,
                                           'role': 'instructor',
                                           'form': form})


@login_required(login_url="/login/")
@permission_required('SDP.instructor', login_url="/no_permission")
def open_course(request, course_id):
    me = whoami(request.user.id)
    course = Course.objects.filter(course_id=course_id)
    if course:
        Course.objects.filter(course_id__exact=course_id).update(open=True)
        return redirect("/modify_course/" + course_id)
    else:
        HttpResponse("No such course")


@login_required(login_url="/login/")
def next_module(request, course_id):
    me = whoami(request.user.id)
    course = Course.objects.filter(course_id=course_id)
    if course:
        enrollment = Enrollment.objects.filter(employee=me, course=course[0])
        total_module = Module.objects.filter(course_id=course_id).count()
        if enrollment[0].progress == total_module:
            enrollment.update(completed=True, completed_date=datetime.date.today())
            return redirect("/home/")
        else:
            enrollment.update(progress=F('progress') + 1)
            return redirect("/course/" + course_id)
    else:
        HttpResponse("No such course")


@login_required(login_url="/login/")
def enrol(request, course_id):
    me = whoami(request.user.id)
    unfinished = Enrollment.objects.filter(employee=me, completed=False)
    course_enrolled = Enrollment.objects.filter(employee=me, course__course_id=course_id)
    if course_enrolled:
        course_completed = course_enrolled.filter(completed=True)
        if course_completed and len(unfinished) > 0:
            return HttpResponse("You can enroll in at most one course.")
        else:
            drop(request, course_id)
            enrol(request, course_id)
            return redirect("/")
    else:
        if len(unfinished) == 0:
            new_enrol = Enrollment.objects.create(course_id=course_id, employee=me, progress=1)
            new_enrol.save()
            return redirect("/")
        else:
            return HttpResponse("You can enroll in at most one course.")


@login_required(login_url="/login/")
def drop(request, course_id):
    me = whoami(request.user.id)
    enrollment_info = Enrollment.objects.filter(employee=me, course__course_id=course_id)
    if enrollment_info:
        Enrollment.objects.filter(course_id=course_id, employee=me).delete()
        redirect("/home/")
    return redirect("/")


@login_required(login_url="/login/")
@permission_required('SDP.HR', login_url="/no_permission")
def record(request):
    me = whoami(request.user.id)
    if request.method == 'POST':
        form = RecordForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            user = User.objects.filter(username=username)
            if not user:
                return HttpResponse("No such user.")
            employee = Employee.objects.filter(user=user[0])
            enrollment_info = Enrollment.objects.filter(employee=employee, completed=True)
            completed_courses = []
            for enrollment in enrollment_info:
                completed_courses.append((enrollment.course, enrollment.completed_date))
            return render(request, 'record.html', {'whoami': me,
                                                   'completed_courses': completed_courses,
                                                   'username': username,
                                                   'role': 'HR'})
    else:
        form = RecordForm()
        return render(request, 'record_form.html', {'whoami': me,
                                                    'form': form,
                                                    'role': 'HR'})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            employee_name = request.POST['employee_name']
            username = request.POST['username']
            password = request.POST['password']
            password_again = request.POST['password_again']
            if not password == password_again:
                return HttpResponse("Password doesn't match")
            if not (len(username) == 8 and re.match("^[A-Za-z0-9_-]*$", username)):
                return HttpResponse(
                    "Usernames are 8-character ids containing only letters, digits, dashes and underscores")
            new_user = User.objects.create_user(username, None, password)
            new_user.save()
            new_employee = Employee.objects.create(employee_name=employee_name, user=new_user)
            new_employee.save()
            return redirect("/")
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'categories': Category.objects.all(),
                                             'form': form})


@login_required(login_url="/login/")
def role(request):
    me = whoami(request.user.id)
    is_admin = True if Administrators.objects.filter(employee=me) else False
    is_instructor = True if Instructor.objects.filter(employee=me) else False
    is_HR = True if HR.objects.filter(employee=me) else False
    return render(request, 'role.html', {'categories': Category.objects.all(),
                                         'whoami': me,
                                         'is_admin': is_admin,
                                         'is_instructor': is_instructor,
                                         'is_HR': is_HR})


@login_required(login_url="/login/")
@permission_required('SDP.admin', login_url="/no_permission")
def manage_category(request):
    me = whoami(request.user.id)
    if request.method == 'POST':
        form = AddCategoryForm(request.POST)
        if form.is_valid():
            catname = request.POST['catname']
            new_category = Category.objects.create(category_name=catname)
            new_category.save()
            return redirect("/home_admin/")
    else:
        form = AddCategoryForm()
    return render(request, 'manage_category.html', {'whoami': me,
                                                    'role': 'administrator',
                                                    'form': form})


def no_permission(request):
    return HttpResponse("You don't have permission to read this page.")
