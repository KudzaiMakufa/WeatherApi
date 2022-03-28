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
import pickle
import requests
import json
import csv
from django.conf import settings
from time import sleep

from weatherhadoop.settings import MEDIA_ROOT



@login_required
def dashboard_index(request):
    form = None
    url = "dashboard/index.html" 
    if request.method == 'POST':
        form = Library_Form(request.POST, request.FILES)
        if(form.is_valid()):
            data = form.save(commit=False)
          
        
            
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

    tuples = []
    data = None
    url ="dashboard/library_view.html"
    if library[0].data_mode  == "csv":
        
        df = pd.read_csv(library[0].library_list.path, delimiter=',')
        tuples = [tuple(x) for x in df.values]
    if library[0].data_mode  == "text":
        data_file = open(library[0].library_list.path , 'r')       
        data = '\n'.join(data_file.read())
        url="dashboard/library_view_text.html"
        
    context = {
        "item":library[0], 
        "lines":tuples,
        "text_file":data
    }
    return render(request, url, context)

@login_required
def view_data(request , lib_id=None):
    library = Library.objects.get(id=lib_id)

    title = ""
    data = []
    print()

    if library.data_mode  == "api":
        response = requests.get('https://api.openweathermap.org/data/2.5/forecast?id=890299&units=metric&appid=9b63dca2ced4e2d6ad7f4f01698d7a45')
        if response.status_code == 200 and 'application/json' in response.headers.get('Content-Type',''):
            result = response.json()
            data = result['list']
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
def map_data(request):
    csv_file = Library.objects.get(data_mode="csv")
    title = "Mapping Uploaded Data"  
    data = []
    csv_file.library_list.path
    # if library.data_mode  == "csv":
    data = pd.read_csv(csv_file.library_list.path)

    print("1111111111+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    #Slicing Data
    slice1 = data.iloc[0:399,:]
    slice2 = data.iloc[400:800,:]
    slice3 = data.iloc[801:1200,:]
    slice4 = data.iloc[1201:,:]

    print("22222222222+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    def mapper(data):
        mapped = []
        for index,row in data.iterrows():
            mapped.append((row['Data.Temperature.Max Temp'],row['Data.Temperature.Avg Temp'] ))
        return mapped
    map1 = mapper(slice1)
    map2 = mapper(slice2)
    map3 = mapper(slice3)
    map4 = mapper(slice4)

    shuffled = {
        3.0: [],
        4.0: [],
        5.0: [],
        6.0: [],
        7.0: [],
        8.0: [],
        
    }

    print("3333333333333+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    try:
        for i in [map1,map2,map3,map4]:
            for j in i:
                shuffled[j[0]].append(j[1])
    except:
        pass


    filename = MEDIA_ROOT+"/"+csv_file.application_name+' shuffled.pkl'
    file= open(filename,'ab')
    pickle.dump(shuffled,file)
    file.close()

 
    context = {
        "file_id":csv_file.application_name+' shuffled.pkl' ,
        "section":"mapper",
        "title":title
       
    }
    # sleep(6)
    messages.add_message(request, messages.INFO, 'Data has been mapped and serialized in folder in '+filename+' \n Please proceed to reduce data')
    return render(request, "dashboard/merge.html", context)
@login_required


@login_required
def reduce_data(request , file_id=None):
    import pickle

    file= open(MEDIA_ROOT+"/"+file_id,'rb')

    print(file)
    shuffled = pickle.load(file)

    def reduce(shuffled_dict):
        reduced = {}
        
        try:
            for i in shuffled_dict: 
           
                reduced[i] = sum(shuffled_dict[i])/len(shuffled_dict[i])
                pass
            return reduced
        except:
            pass


    final = reduce(shuffled)

    try:
        for i in final:

            print(i,':',final[i])
    except:
            pass

    context = {
        # "item":library,
        # "data":data ,
        "section":"reducer",
        "title":"Reduce Functinality"
       
    }
    # sleep(6)
    messages.add_message(request, messages.INFO, 'Reduce Functioanlity successfully executed based on different dataset slices')
    return render(request, "dashboard/merge.html", context)
        
@login_required
def process_data(request):
    # library = Library.objects.get(id=lib_id)

    csv_file = Library.objects.get(data_mode="csv")

    title = ""
    
    data = []
    print()

    # merge data from csv

    # if library.data_mode  == "text":
    #     f = open(library.library_list.path, "r")
    #     print("text")
    #     title = "Hadoop map reduce operation from Text "

    # if library.data_mode  == "csv":
    #     f = open(library.library_list.path, "r")
      
    # convert csv file to text 
    with open(settings.HADOOP_ROOT+"/merged_file.txt", "w") as my_output_file:
        with open(csv_file.library_list.path, "r") as my_input_file:
            [ my_output_file.write(" ".join(row)+'\n') for row in csv.reader(my_input_file)]
        my_output_file.close()
    
    # open the new file and append txt file 


    
    # if library.data_mode  == "api":
    #     response = requests.get('https://api.openweathermap.org/data/2.5/forecast?id=890299&units=metric&appid=9b63dca2ced4e2d6ad7f4f01698d7a45')
    #     if response.status_code == 200 and 'application/json' in response.headers.get('Content-Type',''):
    #         result = response.json()
    #         data = result['list']

    #         # apply hadoop 

    #         # save to db 


    #     else:
    #         print("error loading info")
    #     title = "Pulling 5 Day data focused for Harare before Hadoop implementation   "
    context = {
        # "item":library,
        # "data":data ,
        # "title":title
       
    }
    sleep(6)
    messages.add_message(request, messages.INFO, 'Merge successful ,  file store in '+settings.HADOOP_ROOT+"/merged_file.txt")
    return render(request, "dashboard/merge.html", context)
@login_required
def delete_librabry(request ,librabry_id=None):
    library = Library.objects.get(pk=librabry_id)
    library.delete()
    messages.add_message(request, messages.INFO, 'Library deleted')
    return HttpResponseRedirect('/dashboard/libraries')

