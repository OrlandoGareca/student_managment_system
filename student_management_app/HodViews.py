import datetime

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from student_management_app.models import CustomUser, Courses, Subjects, Staffs, Students


def admin_home(request):
    return render(request, "hod_templates/home_content.html")


def add_staff(request):
    return render(request, "hod_templates/add_staff_template.html")


def add_staff_save(request):
    if request.method != "POST":
        return HttpResponse("Method not Allowed")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        address = request.POST.get("address")
        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email,
                                                  last_name=last_name,
                                                  first_name=first_name, user_type=2)
            user.staffs.address = address
            user.save()
            messages.success(request, "Staff Añadido Satisfactoriamente")
            return HttpResponseRedirect("/add_staff")
        except:
            messages.error(request, "Staff no se añadio")
            return HttpResponseRedirect("/add_staff")


def add_course(request):
    return render(request, "hod_templates/add_course_template.html")


def add_course_save(request):
    if request.method != "POST":
        return HttpResponseRedirect("Method Not Allowed")
    else:
        course = request.POST.get("course")
        try:
            course_model = Courses(course_name=course)
            course_model.save()
            messages.success(request, "Curso Añadido Satisfactoriamente")
            return HttpResponseRedirect("/add_course")
        except:
            messages.error(request, "Curso no se añadio")
            return HttpResponseRedirect("/add_course")


def add_student(request):
    courses = Courses.objects.all()
    return render(request, "hod_templates/add_student_template.html", {"courses": courses})


def add_student_save(request):
    if request.method != "POST":
        return HttpResponse("Method not Allowed")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        address = request.POST.get("address")
        session_start = request.POST.get("session_start")
        session_end = request.POST.get("session_end")
        course_id = request.POST.get("course")
        sex = request.POST.get("sex")

        profile_pic = request.FILES['profile_pic']
        fs = FileSystemStorage()
        filename = fs.save(profile_pic.name, profile_pic)
        profile_pic_url = fs.url(filename)
        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email,
                                                  last_name=last_name,
                                                  first_name=first_name, user_type=3)
            user.students.address = address
            course_obj = Courses.objects.get(id=course_id)
            user.students.course_id = course_obj
            user.students.session_start_year = session_start
            user.students.session_start_end = session_end
            user.students.gender = sex
            user.students.profile_pic = profile_pic_url
            user.save()
            messages.success(request, "Estudiante Añadido Satisfactoriamente")
            return HttpResponseRedirect("/add_student")
        except:
            messages.error(request, "Estudiante no se añadio")
            return HttpResponseRedirect("/add_student")


def add_subject(request):
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    return render(request, "hod_templates/add_subject_template.html", {"staffs": staffs, "courses": courses})


def add_subject_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method not Allowed</h2>")
    else:
        subject_name = request.POST.get("subject_name")
        course_id = request.POST.get("course")
        course = Courses.objects.get(id=course_id)
        staff_id = request.POST.get("staff")
        staff = CustomUser.objects.get(id=staff_id)

        try:
            subject = Subjects(subject_name=subject_name, course_id=course, staff_id=staff)
            subject.save()
            messages.success(request, "Subject Añadido Satisfactoriamente")
            return HttpResponseRedirect("/add_subject")
        except:
            messages.error(request, "Subject no se añadio")
            return HttpResponseRedirect("/add_subject")


def manage_staff(request):
    staffs = Staffs.objects.all()
    return render(request, "hod_templates/manage_staff_template.html", {"staffs": staffs})


def manage_student(request):
    students = Students.objects.all()
    return render(request, "hod_templates/manage_student_template.html", {"students": students})


def manage_course(request):
    courses = Courses.objects.all()
    return render(request, "hod_templates/manage_course_template.html", {"courses": courses})


def manage_subject(request):
    subjects = Subjects.objects.all()
    return render(request, "hod_templates/manage_subject_template.html", {"subjects": subjects})


def edit_staff(request, staff_id):
    staff = Staffs.objects.get(admin=staff_id)
    return render(request, "hod_templates/edit_staff_template.html", {"staff": staff,"id":staff_id})


def edit_staff_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        staff_id = request.POST.get("staff_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        address = request.POST.get("address")
        try:
            user = CustomUser.objects.get(id=staff_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()
            staff_model = Staffs.objects.get(admin=staff_id)
            staff_model.address = address
            staff_model.save()
            messages.success(request, "Staff Editado Satisfactoriamente")
            return HttpResponseRedirect("/edit_staff/" + staff_id)
        except:
            messages.error(request, "Staff no se edito")
            return HttpResponseRedirect("/edit_staff/" + staff_id)


def edit_student(request, student_id):
    courses = Courses.objects.all()
    student = Students.objects.get(admin=student_id)
    return render(request, "hod_templates/edit_student_template.html", {"student": student, "courses": courses,"id":student_id})


def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        student_id = request.POST.get("student_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")

        address = request.POST.get("address")
        session_start = request.POST.get("session_start")
        session_end = request.POST.get("session_end")
        course_id = request.POST.get("course")
        sex = request.POST.get("sex")

        if request.FILES.get('profile_pic', False):
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
        else:
            profile_pic_url = None

        try:
            user = CustomUser.objects.get(id=student_id)
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.email = email
            user.save()

            student = Students.objects.get(admin=student_id)
            student.address = address
            student.session_start_year = session_start
            student.session_start_end = session_end
            student.gender = sex
            if profile_pic_url != None:
                student.profile_pic = profile_pic_url

            course = Courses.objects.get(id=course_id)
            student.course_id = course
            student.save()
            messages.success(request, "Student Editado Satisfactoriamente")
            return HttpResponseRedirect("/edit_student/" + student_id)
        except:
            messages.error(request, "Student no se edito")
            return HttpResponseRedirect("/edit_student/" + student_id)


def edit_subject(request, subject_id):
    subject = Subjects.objects.get(id=subject_id)
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    return render(request, "hod_templates/edit_subject_template.html",
                  {"subject": subject, "courses": courses, "staffs": staffs,"id":subject_id})


def edit_subject_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_id = request.POST.get("subject_id")
        subject_name = request.POST.get("subject_name")
        staff_id = request.POST.get("staff")
        course_id = request.POST.get("course")
        try:
            subject = Subjects.objects.get(id=subject_id)
            subject.subject_name = subject_name
            staff = CustomUser.objects.get(id=staff_id)
            subject.staff_id = staff
            course = Courses.objects.get(id=course_id)
            subject.course_id = course
            subject.save()

            subject.save()
            messages.success(request, "Subject Editado Satisfactoriamente")
            return HttpResponseRedirect("/edit_subject/" + subject_id)
        except:
            messages.error(request, "Subject no se edito")
            return HttpResponseRedirect("/edit_subject/" + subject_id)


def edit_course(request, course_id):
    course = Courses.objects.get(id=course_id)
    return render(request, "hod_templates/edit_course_template.html", {"course": course,"id":course_id})


def edit_course_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        course_id = request.POST.get("course_id")
        course_name = request.POST.get("course")
        try:
            course = Courses.objects.get(id=course_id)
            course.course_name = course_name
            course.save()
            messages.success(request, "Course Editado Satisfactoriamente")
            return HttpResponseRedirect("/edit_course/" + course_id)
        except:
            messages.error(request, "Course no se edito")
            return HttpResponseRedirect("/edit_course/" + course_id)
