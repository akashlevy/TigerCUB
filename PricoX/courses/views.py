from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from courses.models import tags

def login_user(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render_to_repsonse('course_picker.html')
        else:
            return render_to_response('auth.html', {"error" : "Username/password incorrect"})

    return render_to_response('auth.html')

def course_picker(request):
    global tags
    return render_to_response('course_picker.html', {"tags" : tags})
            
            
