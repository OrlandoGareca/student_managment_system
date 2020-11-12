from django.shortcuts import render

# from student_management_app.models import Students, Courses, Subjects


def student_home(request):
    return render(request,"student_template/student_home_template.html")

#
# def student_view_attendance(request):
#     # student=Students.objects.get(admin=request.user.id)
#     # course=Courses.objects.get(idd=student.course_id.id)
#     # subjects=Subjects.objects.filter(course_id=course)
#     return render(request,"student_template/student_view_attendance.html")