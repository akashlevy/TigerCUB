from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from courses.models import tags

def login_user(request):
    state = ""
    username = password = ''
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        print username
        print password

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "Your username and/or password were incorrect."
    if request.user.is_authenticated():
        return render(request, 'course_picker.html', {'tags':tags})
    else:
        return render(request, 'auth.html', {'state':state, 'username': username})
        
def logout_user(request):
    logout(request)
    return redirect('/')