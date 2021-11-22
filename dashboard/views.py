from django.shortcuts import render
import calendar
from datetime import datetime
from django.contrib.auth.decorators import login_required , permission_required
from django.urls.base import translate_url
from pypi_simple import PyPISimple 
from dashboard.forms import Library_Form , CVE_Scan_Form
from dashboard.models import  Library
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse
from django.http import HttpResponseRedirect
import vulners  
from django.core.mail import send_mail
import random
import pandas as pd
import requests
import json



# @login_required
# def dashboard_index(request):

    
    
#     url = "dashboard/index.html"    
#     with PyPISimple() as client:
#         requests_page = client.get_project_page('requests')
#     requests_page = client.get_project_page('requests')
#     pkg = requests_page.packages[0]
#     print(pkg.version)
    
#     context = {
#         'title': pkg.version,
       
        
      
#     }

#     return render(request , url , context) 

@login_required
def dashboard_index(request):
    form = None
    url = "dashboard/index.html" 
    if request.method == 'POST':
        form = Library_Form(request.POST, request.FILES)
        if(form.is_valid()):
            data = form.save(commit=False)
          
            # if data.data_mode  == "csv":
            #     print("csv")
            
            # if data.data_mode  == "text":
            #     print("text")
            # if data.data_mode  == "api":
            #     print("api")
            
            data.created_at = timezone.now()
            data.updated_at = timezone.now()
            data.created_by = request.user.id   
            data.save()
            messages.add_message(request, messages.INFO, 'Application Libraries stored successful')
            return HttpResponseRedirect(reverse('dashboard:libraries'))
     
    else:
        form = Library_Form()
    
    context = {
        
        'title': "Pull Data",
        'form':form
        
    } 
     
    return render(request , url , context)


def send_notification(request ):

    send_mail(
        'Out of boundary ',
        'Vehicle abw 1339 is off route on coordinates 18.0.0.7 , 15.0.0.4',
        'magadaline@magtracker.com',
        ['kmakufa@outlook.com', 'r1811075y@students.msu.ac.zw'],
        fail_silently=False,
    )

    return HttpResponseRedirect('http://102.37.108.206/magtracker')

def generate_otp(request):
    number = random.randint(100000,999999)
    send_mail(
        'OTP Password',
        'Your generated unlock code is '+str(number)+' \n MagTracker Capstone Design Project',
        'magadaline@magtracker.com',
        ['kmakufa@outlook.com'],
        fail_silently=False,
    )

    return HttpResponseRedirect('http://102.37.108.206/magtracker')

def alert_recovery(request):

    send_mail(
        'Recovery Needed ',
        'Vehicle abw 1339 has been stationery on location  18.0.0.7 , 15.0.0.4 , render assistance',
        'magadaline@magtracker.com',
        ['kmakufa@outlook.com', 'r1811075y@students.msu.ac.zw'],
        fail_silently=False,
    )

    return HttpResponseRedirect('http://102.37.108.206/magtracker')


def dashboard_libraries(request):
    libraries = Library.objects.all().order_by('-id')
    url = "dashboard/list_librabries.html" 
    # send_mail(
    #     'Payment',
    #     'find payment.',
    #     'kidkudzy@gmail.com',
    #     ['kmakufa@outlook.com', 'promiseksystems@gmail.com'],
    #     fail_silently=False,
    # )
    context = {
        
        'title': "DATA FILES",
        'libraries':libraries
        
    } 


    return render(request , url , context)



@login_required
def library_scan(request ,lib_id=None):
    library = Library.objects.filter(id=lib_id).order_by('-id')
    # f = open(library[0].library_list.path, "r")
    # print("------------------")

    # lines = f.readlines()


    
    # # for line in lines:
    # #     print(line)
    # # print("------------------")
    # f.close()

    # _________________________________
    df = pd.read_csv(library[0].library_list.path, delimiter=',')
    tuples = [tuple(x) for x in df.values]

   
    context = {
        "item":library[0], 
        "lines":tuples,
    }
    return render(request, 'dashboard/library_view.html', context)
    
    
@login_required
def process_data(request ,lib_id=None):
    library = Library.objects.get(id=lib_id)
    title = ""
    
    data = []
    print()
    if library.data_mode  == "csv":
        f = open(library.library_list.path, "r")
        print("csv")
        title = "Hadoop map reduce operation from CSV "

    if library.data_mode  == "text":
        f = open(library.library_list.path, "r")
        print("text")
        title = "Hadoop map reduce operation from Text "
    if library.data_mode  == "api":
        response = requests.get('https://api.openweathermap.org/data/2.5/forecast?id=890299&units=metric&appid=9b63dca2ced4e2d6ad7f4f01698d7a45')
        if response.status_code == 200 and 'application/json' in response.headers.get('Content-Type',''):
            result = response.json()
            data = result['list']

            # apply hadoop 

            # save to db 


        else:
            print("error loading info")
        title = "Pulling 5 Day data focused for Harare before Hadoop implementation   "
    context = {
        "item":library,
        "data":data ,
        "title":title
       
    }
    return render(request, "dashboard/api_process.html", context)
@login_required
def delete_librabry(request ,librabry_id=None):
    library = Library.objects.get(pk=librabry_id)
    library.delete()
    messages.add_message(request, messages.INFO, 'Library deleted')
    return HttpResponseRedirect('/dashboard/libraries')

@login_required
def cve_scan(request):
    form = None
    url = "dashboard/view_by_cve.html" 
    cve_data = []
    if request.method == 'POST':
        url = "dashboard/cve_results.html"
        form = CVE_Scan_Form(request.POST)
        if(form.is_valid()):
           
            data = form.cleaned_data['cve_name']
            print("^^^^^^^^^^^")

            vulners_api = vulners.Vulners(api_key="4QIYDKA0NXPHUWXJNQYLISIZEZZH8FM25YNK0L518VOWJJEOWO81XGMH2KSL81KJ")
            cve_data = vulners_api.document(data)
            print(cve_data)
        
     
    else:
        form = CVE_Scan_Form()
    
    context = {
        
        'title': "Scan by Cve",
        'form':form,
        'cve_data':cve_data
        
    } 
     
    return render(request , url , context)