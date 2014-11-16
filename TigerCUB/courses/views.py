from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from courses.models import tags, UserProfile, Term, Subject

def login_user(request):
    if not request.user.is_authenticated():
        state = ""
        username = password = ''
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    UserProfile.objects.get_or_create(user=user, userYear=0)
                else:
                    state = "Your account is not active, please contact the site admin."
            else:
                state = "NetID/password incorrect."
        if request.user.is_authenticated():
            return render(request, 'course_picker.html', {'tags':tags})
        else:
            return render(request, 'auth.html', {'state':state, 'username':username})
    else:
        state = ""
        courseTable = [[""]*8,[""]*8,[""]*8,[""]*8,[""]*8,[""]*8]
        if request.method == "POST":
            request.user.get_profile().major = request.POST['major']
            userYear = int(request.POST['userYear'])
            department = request.POST['department']
            courseNum = request.POST['courseNum']
            courseYear = int(request.POST['courseYear'])
            courseSem = int(request.POST['courseSem'])
            termNumber = 1152 - (userYear-courseYear)*10 + 2*courseSem
            term = Term.objects.get(code=termNumber)
            courseSubject = None
            for subject in term.subjects:
                if subject.deptCode == department:
                    courseSubject = subject
            theCourse = None
            for course in courseSubject.courses:
                if course.catalogNumber == courseNum:
                    theCourse = course
            if theCourse is None:
                state = "The course specified could not be found"
            else:
                if termNumber in request.user.get_profile().coursesTaken:
                    request.user.get_profile().coursesTaken[termNumber].append(theCourse)
                else:
                    request.user.get_profile().coursesTaken[termNumber] = [theCourse]
        
            startTerm = 1152 - 10*userYear
            termsInCollege = []
            for i in range(8):
                if (i%2 == 0):
                    termsInCollege.append(startTerm + i/2*10)
                else:
                    termsInCollege.append(startTerm + i/2*10 + 2)
            print termsInCollege
            for j in range(6):
                for i in range(8):
                    for courseTaken in request.user.get_profile().coursesTaken.iteritems():
                        if courseTaken[0] == termsInCollege[i] and len(courseTaken[1]) > j:
                            courseTable[j][i] = unicode(courseTaken[1][j])
                            j+=1
                            i=0
                        else:
                            courseTable[j][i] = ""
            print courseTable
        return render(request, 'course_picker.html', {'tags':tags,'state':state,'courseTable':courseTable})
        
def logout_user(request):
    logout(request)
    return redirect('/')
    