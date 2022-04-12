from django.shortcuts import render
import io

import requests
from rest_framework.parsers import JSONParser
from .models import Student
from .serializers import StudentSerializer
from django.http import JsonResponse
from rest_framework.renderers import JSONRenderer #To convert python data from python native(dictionary) to JSON
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def student_api(request):
    #print("inside*******************request**************")
    #print(request)
    if request.method == 'GET':
        json_data=request.body #Got the json data
        #print(json_data)
        stream=io.BytesIO(json_data)
        #print("stream************************************",stream)
        pythondata=JSONParser().parse(stream) #Converting it to python data
        #print("pythondata*************************",pythondata)
        id=pythondata.get('id', None)
        #print("ID****************************",id)
        if id is not None:
            stu=Student.objects.get(id=id)
            serializerr=StudentSerializer(stu) #Complex data to json data
            #Json_data=JSONRenderer().render(serializerr.data)
            #return HttpResponse(Json_data,content_type='application/json')
            return JsonResponse(serializerr.data,safe=False)
        stu=Student.objects.all()
        serializerr=StudentSerializer(stu,many=True)
        #Json_data=JSONRenderer().render(serializerr.data)
        #return HttpResponse(Json_data,content_type='application/json')
        return JsonResponse(serializerr.data,safe=False)
    if request.method=='POST':
        json_data=request.body #Got the json data
        stream=io.BytesIO(json_data)
        pythondata=JSONParser().parse(stream) #Converted to python data
        serializerr=StudentSerializer(data=pythondata) #Converted to complex data
        if serializerr.is_valid(): #If converted data is valid
            serializerr.save() #Svae to the database
            res={'msg':'data created'} #After saving the data this responce will be returned.
            return JsonResponse(res,safe=False) #Send the responce
        return JsonResponse(serializerr.errors,safe=False) #if data is not valid send the error message
    if request.method=='PUT':
        json_data=request.body #Got the json data
        stream=io.BytesIO(json_data)
        pythondata=JSONParser().parse(stream) #Converted to python data
        id=pythondata.get('id') #Getting the ID which client has sent for update
        stu=Student.objects.get(id=id) #Getting the data from database using the ID which is sent by client
        #If we remove partial =True it will expect all the fields to be updated.
        serializerr=StudentSerializer(stu,data=pythondata,partial=True) #Converted to complex data to update the database partially
        if serializerr.is_valid(): #If converted data is valid
            serializerr.save() #Svae to the database
            res={'msg':'data updated successfully!!!'} #After saving the data this responce will be returned.
            return JsonResponse(res,safe=False) #Send the responce
        return JsonResponse(serializerr.errors,safe=False) #if data is not valid send the error message
    if request.method=='DELETE':
        json_data=request.body
        json_data=request.body #Got the json data
        stream=io.BytesIO(json_data)
        pythondata=JSONParser().parse(stream) #Converted to python data
        id=pythondata.get('id') #Getting the ID which client has sent for update
        stu=Student.objects.get(id=id) #Getting the data from database using the ID which is sent by client
        stu.delete()
        res={'msg':'data deleted successfully!!!'}
        return JsonResponse(res,safe=False) #Send the responce

'''
def student_api_all(request):
    User=Student.objects.all()
    serializerr=StudentSerializer(User,many=True)
    #Json_data=JSONRenderer().render(serializerr.data)
    #return HttpResponse(Json_data,content_type='application/json') #This will return JSON data
    #same as above two lines
    return JsonResponse(serializerr.data,safe=False) #This will aslo return JSON data 
    #return Response(serializerr.data)
'''