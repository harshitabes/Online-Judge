from django.shortcuts import render
from .models import Problem
import requests

# Create your views here.

def home(request):
    var=Problem.objects.all()
    context={'data':var}

    return render(request,'ide/homepage.html',context)



def submit(request):

    return render(request,'ide/front.html')



def process(request):
    if request.method == 'POST':
        code=request.POST.get('sourcecode')
        langid=request.POST.get('lang')

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
    y1=r.json()['status']['description']
    y2=r.json()['time']
    context={'Submission_Result': y1, 'Time_Taken': y2}
    return render(request,'ide/result.html',context)





