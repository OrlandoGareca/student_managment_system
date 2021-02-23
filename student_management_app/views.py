from django.contrib import messages
from django.contrib.auth import  login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from student_management_app.EmailBackEnd import EmailBackEnd


def shwDemoPage(request):
    return render(request, "demo.html")


def ShowLoginPage(request):
    return render(request, "login_page.html")


def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method not Allowed</h2>")
    else:
        user = EmailBackEnd.authenticate(request, username=request.POST.get("email"),password=request.POST.get("password"))
        if user != None:
            login(request,user)
            if user.user_type=="1":
                return HttpResponseRedirect(reverse('admin_home'))
            elif user.user_type=="2":
               return HttpResponseRedirect(reverse("staff_home"))
            else:
               return HttpResponseRedirect(reverse("student_home"))
            # return HttpResponseRedirect('/admin_home')
            # return HttpResponse("Email : " + request.POST.get("email") + "Password : " + request.POST.get("password"))
        else:
            messages.error(request,"Inicio Sesion Invalido Detalles")
            return HttpResponseRedirect("/")


def GetUserDetails(request):
    if request.user != None:
        return HttpResponse("User :" + request.user.email + " usertype : " + request.user.user_type)
    else:
        return HttpResponse("Por Favor inicie sesion primero")


def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")


def showFirebaseJs(request):
    data = 'importScripts("https://www.gstatic.com/firebasejs/7.14.6/firebase-app.js");' \
           'importScripts("https://www.gstatic.com/firebasejs/7.14.6/firebase-messaging.js"); ' \
           'var firebaseConfig = {' \
           '        apiKey: "YOUR_API_KEY",' \
           '        authDomain: "FIREBASE_AUTH_URL",' \
           '        databaseURL: "FIREBASE_DATABASE_URL",' \
           '        projectId: "FIREBASE_PROJECT_ID",' \
           '        storageBucket: "FIREBASE_STORAGE_BUCKET_URL",' \
           '        messagingSenderId: "FIREBASE_SENDER_ID",' \
           '        appId: "FIREBASE_APP_ID",' \
           '        measurementId: "FIREBASE_MEASUREMENT_ID"' \
           ' };' \
           'firebase.initializeApp(firebaseConfig);' \
           'const messaging=firebase.messaging();' \
           'messaging.setBackgroundMessageHandler(function (payload) {' \
           '    console.log(payload);' \
           '    const notification=JSON.parse(payload);' \
           '    const notificationOption={' \
           '        body:notification.body,' \
           '        icon:notification.icon' \
           '    };' \
           '    return self.registration.showNotification(payload.notification.title,notificationOption);' \
           '});'

    return HttpResponse(data, content_type="text/javascript")