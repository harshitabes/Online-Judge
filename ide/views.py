from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Problem
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from .models import UserDetail, Submissions
from rest_framework import viewsets
from .serializers import UserDetailSerializer
import requests


# Create your views here.
def home(request):
    return render(request, 'ide/homepage.html')


def loginview(request):
    if request.method == 'POST':
        name = request.POST['username']
        pas = request.POST['password']
        user = authenticate(username=name, password=pas)
        if user is not None:
            login(request, user)
            return redirect('contest')
        else:
            return redirect('home')


def Signup(request):
    if request.method == 'POST':
        name = request.POST['username']
        pas = request.POST['password']
        mail = request.POST['mail']
        user = User.objects.create_user(name, mail, pas)
        user.save()
        user.is_active = False

        current_site = get_current_site(request)
        mail_subject = 'Please click the link to activate your Codeplatform account.You will be automatically logged in to Codeplatform'
        message = render_to_string('ide/acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            'token': account_activation_token.make_token(user),
        })

        to_email = request.POST['mail']

        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        return HttpResponse('Please confirm your email address to complete the registration')





    else:
        return render(request, 'ide/signup.html')


class UserDetailViewSet(viewsets.ModelViewSet):
    queryset = UserDetail.objects.all()
    serializer_class = UserDetailSerializer


def user_detail(request, id):
    userinfo = UserDetail.objects.filter(username=id)
    if len(userinfo):
        info = UserDetail.objects.get(username=id)
        problems_solved = Submissions.objects.filter(user=info)
        problems_done = []
        for i in range(0, len(problems_solved)):
            problems_done.append(problems_solved[i].problem.title)
        context = {'data': info, 'problems_done': problems_done}
        print(info)
        print(info.name)
    else:
        return HttpResponse("User does not exist")

    return render(request, 'ide/user.html', context)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')

    else:
        return HttpResponse('Activation link is invalid!')


def logoutview(request):
    logout(request)
    return redirect('home')


def contest(request):
    if not request.user.is_authenticated:
        return redirect('home')
    var = Problem.objects.all()
    context = {'data': var}

    # return HttpResponse(var.statement)
    return render(request, 'ide/contest.html', context)


def submit(request, pk):
    if not request.user.is_authenticated:
        return redirect('home')
    # request.add("skjd","hkwh")
    stri = "/submit/" + str(pk) + "/result/"
    context = {'data': stri}
    return render(request, 'ide/front.html', context)


def process(request, pk):
    if not request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        code = request.POST.get('sourcecode')
        langid = request.POST.get('lang')

    URL = "https://api.judge0.com/submissions?base64_encoded=false&wait=true"

    with open("inputfile.txt", "r") as myfile:
        input = myfile.read()

    with open("outputfile.txt", "r") as myfile:
        output = myfile.read()

    data = {
        # "source_code": "x=int(input())\nif x%2==0:\n\tprint('even')\nelse:\n\tprint('odd')",
        "source_code": code,
        "language_id": langid,
        "number_of_runs": "1",
        "stdin": input,
        "expected_output": output,
        "cpu_time_limit": "2",
        "cpu_extra_time": "0.5",
        "wall_time_limit": "5",
        "memory_limit": "128000",
        "stack_limit": "64000",
        "max_processes_and_or_threads": "30",
        "enable_per_process_and_thread_time_limit": 'False',
        "enable_per_process_and_thread_memory_limit": 'True',
        "max_file_size": "1024"
    }

    r = requests.post(url=URL, json=data)
    '''print(r.json())
    print("Submission Result : %s" % r.json()['status']['description'])
    print("Time Taken : %s" % r.json()['time'])'''
    y1 = r.json()['status']['description']
    print(request.user)
    if y1 == "Accepted":
        userobj = UserDetail.objects.get(username=request.user.username)
        problem = Problem.objects.get(pk=pk)
        Submissions.objects.create(user=userobj, problem=problem)
    y2 = r.json()['time']
    context = {'Submission_Result': y1, 'Time_Taken': y2}
    return render(request, 'ide/result.html', context)
