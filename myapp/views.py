from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,get_object_or_404, redirect
from django import template
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from datetime import datetime
from myapp.forms import Authentic
from django.conf import settings
import cv2
import os
import operator
from .forms import *
from .models import *
from django_otp.oath import totp
import time
import base64
from myapp import path
from path import *
from scipy import misc
import cv2
import numpy as np
from PIL import Image
import glob
from collections import defaultdict
from myapp import facenet
from myapp import detect_face
import os
import time
import pickle
from PIL import Image
import glob
from twilio.rest import Client
account_sid = 'AC730d2142614ea4d8220278bb5bd247fd'
auth_token = 'fdd8833312fe3d2ebc9eb7142c3cb771'
##################################################################
# account_sid = 'ACf896cacf87342b00d224a999be391e7e'
# auth_token = 'c26c67fbb8193ebb4cec3a8364469a4a'
client = Client(account_sid, auth_token)

def sms(msg, phn_number):
	message = client.messages \
	                .create(
	                     body=str(msg),
	                     from_='+15093977702',
	                     # from_='+15017122661',
	                     to='+91'+ str(phn_number)
	                 )

	print(message.sid)

def call(phn):
	call = client.calls.create(
	                        twiml='<Response><Say>Alert!, You have a request</Say></Response>',
	                        to='+91'+str(phn),
	                        from_='+15093977702'
	                    )

	print(call.sid)
######################################################################################################################
def create_data_model():
    data = {}
    data['distance_matrix'] = [
        [
            0, 548, 776, 696, 582, 274, 502, 194, 308, 194, 536, 502, 388, 354,
            468, 776, 662
        ],
        [
            548, 0, 684, 308, 194, 502, 730, 354, 696, 742, 1084, 594, 480, 674,
            1016, 868, 1210
        ],
        [
            776, 684, 0, 992, 878, 502, 274, 810, 468, 742, 400, 1278, 1164,
            1130, 788, 1552, 754
        ],
        [
            696, 308, 992, 0, 114, 650, 878, 502, 844, 890, 1232, 514, 628, 822,
            1164, 560, 1358
        ],
        [
            582, 194, 878, 114, 0, 536, 764, 388, 730, 776, 1118, 400, 514, 708,
            1050, 674, 1244
        ],
        [
            274, 502, 502, 650, 536, 0, 228, 308, 194, 240, 582, 776, 662, 628,
            514, 1050, 708
        ],
        [
            502, 730, 274, 878, 764, 228, 0, 536, 194, 468, 354, 1004, 890, 856,
            514, 1278, 480
        ],
        [
            194, 354, 810, 502, 388, 308, 536, 0, 342, 388, 730, 468, 354, 320,
            662, 742, 856
        ],
        [
            308, 696, 468, 844, 730, 194, 194, 342, 0, 274, 388, 810, 696, 662,
            320, 1084, 514
        ],
        [
            194, 742, 742, 890, 776, 240, 468, 388, 274, 0, 342, 536, 422, 388,
            274, 810, 468
        ],
        [
            536, 1084, 400, 1232, 1118, 582, 354, 730, 388, 342, 0, 878, 764,
            730, 388, 1152, 354
        ],
        [
            502, 594, 1278, 514, 400, 776, 1004, 468, 810, 536, 878, 0, 114,
            308, 650, 274, 844
        ],
        [
            388, 480, 1164, 628, 514, 662, 890, 354, 696, 422, 764, 114, 0, 194,
            536, 388, 730
        ],
        [
            354, 674, 1130, 822, 708, 628, 856, 320, 662, 388, 730, 308, 194, 0,
            342, 422, 536
        ],
        [
            468, 1016, 788, 1164, 1050, 514, 514, 662, 320, 274, 388, 650, 536,
            342, 0, 764, 194
        ],
        [
            776, 868, 1552, 560, 674, 1050, 1278, 742, 1084, 810, 1152, 274,
            388, 422, 764, 0, 798
        ],
        [
            662, 1210, 754, 1358, 1244, 708, 480, 856, 514, 468, 354, 844, 730,
            536, 194, 798, 0
        ],
    ]
    data['demands'] = [0, 1, 1, 2, 4, 2, 4, 8, 8, 1, 2, 1, 2, 4, 4, 8, 8]
    data['vehicle_capacities'] = [15, 15, 15, 15]
    data['num_vehicles'] = 4
    data['depot'] = 0
    return data


def print_solution(data, manager, routing, assignment):
    list1=[]
    total_distance = 0
    total_load = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        route_load = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data['demands'][node_index]
            plan_output += ' {0} Load({1}) -> '.format(node_index, route_load)
            previous_index = index
            index = assignment.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        plan_output += ' {0} Load({1})\n'.format(manager.IndexToNode(index),
                                                 route_load)
        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        plan_output += 'Load of the route: {}\n'.format(route_load)
        print(plan_output)
        list1.append(plan_output)
        total_distance += route_distance
        total_load += route_load
    print('Total distance of all routes: {}m'.format(total_distance))
    print('Total load of all routes: {}'.format(total_load))
    return list1


def main():
    # Instantiate the data problem.
    data = create_data_model()

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)


    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)


    # Add Capacity constraint.
    def demand_callback(from_index):
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return data['demands'][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(
        demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data['vehicle_capacities'],  # vehicle maximum capacities
        True,  # start cumul to zero
        'Capacity')

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    output=[]
    assignment = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if assignment:
        output= print_solution(data, manager, routing, assignment)
    return output


#########################################################################################################################
secret_key = b'12345678901234567890'
now = int(time.time())


def index(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request,'security.html',)
        elif request.user.is_staff:
            return render(request,'staff.html',)
            #return HttpResponseRedirect('/admin/')
        else:
            #pass
            return render(request,'inmates.html',)
            #rreturn HttpResponseRedirect('index')
    else:
        return render(request,'index.html',)

@login_required
def dashboard(request):
    if request.user.is_superuser:
        return render(request,'security.html',)
    elif request.user.is_staff:
        return render(request,'staff.html')
    else:
        return render(request,'inmates.html',)


@login_required
def myupdate(request):
    if request.user.is_superuser:
        pass
    else:
        return HttpResponse("updation", content_type='text/plain')





@login_required
def verify_otp(request):
    if request.user.is_superuser:
        if request.method =='POST':
            username=request.POST.get("username")
            print (username)
            password=request.POST.get("password")
            try:
                originaluser = otp.objects.filter(name=username)
                length = len(originaluser)
                print(length)
                originaluser= originaluser[length-1]
                if originaluser:
                    if originaluser.otp == password:
                        return HttpResponse("verified and allow")
                    else:
                        return HttpResponse("invalid OTP")
            except:
                return HttpResponse("invalid name")


        return render(request,'verify_OTP.html',)
    else:
        return HttpResponse("OTP Verify", content_type='text/plain')


def log(request):
	list1=[]; A=0 ; B =0; C=0 ; indexitem=[]; mydict = {'Area A':0, 'Area B':0, 'Area C':0}
	if request.user.is_superuser or request.user.is_staff:
		results = friendvisitor.objects.values('Location')
		#results = results.values()
		result = results
		for item in result:
			for i in item.values():
				print (i)
				if i=='Area A':
					A= A+1
				elif i=='Area B':
					B= B +1
				elif i =='Area C':
					C = C+1
			#list1.append(item)
		#print(list1)
		mydict['Area A']= A
		mydict['Area B']= B
		mydict['Area C']= C
		sorted_dict = dict(sorted(mydict.items(),key=operator.itemgetter(1),reverse=True))
		print(sorted_dict)


		return render(request,'log.html',{'dictionary':sorted_dict})
		#print(results)
	else:
		return HttpResponse("invalid request")


def decompose(request):
    return render(request,'decompose.html',)


@login_required
def expected(request):
    if request.user.is_superuser:
        return HttpResponse("NOT VALID", content_type='text/plain')
    else:
        if request.method == 'POST':
            form = expectedvis(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return render(request,'inmates.html')
        else:
            form = expectedvis()


        return render(request,'exp.html',{'form' : form})


@login_required
def friend(request):
    if request.user.is_superuser:
        return HttpResponse("NOT VALID", content_type='text/plain')
    else:
        if request.method == 'POST':
            form = friendvis(request.POST, request.FILES)
			#name = request.user.username
            if form.is_valid():
                form.save()
                return render(request,'index.html')
        else:
            form = friendvis()


        return render(request,'friend.html',{'form' : form})


@login_required
def Urgent(request):
    if request.user.is_superuser:
        return HttpResponse("NOT VALID", content_type='text/plain')
    else:
        if request.method == 'POST':
            form = urgentvis(request.POST, request.FILES)
			#name = request.user.username
            if form.is_valid():
                form.save()
                phone = '7639147936'
                #sms("urgent",phone)
                call(phone)
                return render(request,'index.html')
        else:
            form = urgentvis()


        return render(request,'friend_urgent.html',{'form' : form})





@login_required
def myfriend(request):
        if request.user.is_superuser:
            return HttpResponse("NOT VALID", content_type='text/plain')
        else:
            if request.method == 'GET':
                username = request.user.username
                Image2 = friendvisitor.objects.filter(user = username )
                stu = {"details": Image2 }

                return render(request,'myfriend.html',stu)

                if request.method == 'POST':
                    if 'remove' in request.POST :
                        team = friendvisitor.objects.get(id=request.POST.get("student_id"))
                #print (team)
                    team.delete()

            return HttpResponse("Deleted", content_type='text/plain')





@login_required
def awards(request):
    listdetails =[]
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            phn_number = '7639147936'
            call(phn_number)
            # return render(request,'security.html',)
            return redirect("/request_status/")
    else:
        form = UploadForm()


    return render(request,'awards.html',{'form' : form})



@login_required
def top_contributors(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            Image = friendvisitor.objects.values('user').distinct()
            #Image = Image.order_by('-id')
            #print (Image)
            #print(type(Image))

            stu = {"details": Image }
            return render(request,'top.html',stu)
        elif 'pay' in request.POST :
            team = friendvisitor.objects.filter(user=request.POST.get("student_name"))
            i=0
            for i in team:
                if i.reward == 'not paid' and i.status =='allow':
                    i.reward = "paid"
                i.save(update_fields=['reward'])
                i.save()
               # i=i+1
            team = team[0]
            number = team.phone
            number = 7639147936
            message = f"Money is sent to {number}"
            #call(number)
            #sms("money recieved",'7639147936')
            return HttpResponse(message, content_type='text/plain')



#
# @login_required
def path(request):
	 output = main()
	 return HttpResponse(output ,content_type='text/plain')





@login_required
def request_status(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            Image = friendvisitor.objects.all()
            Image = Image.order_by('-id')
            #print (Image)
            #print(type(Image))

            stu = {"details": Image }
            return render(request,'request_status.html',stu)
        if request.method == 'POST':
            if 'reject' in request.POST :
                team = friendvisitor.objects.get(id=request.POST.get("student_id"))

                if team.status == 'allow':
                    team.status = 'pending'
                team.save(update_fields=['status'])
                team.save()

            elif 'accept' in request.POST :
                team = friendvisitor.objects.get(id=request.POST.get("student_id"))
                if team.status == 'pending':
                    team.status = 'allow'
                team.save(update_fields=['status'])
                team.save()

            return HttpResponse("added", content_type='text/plain')


    elif  request.user.is_staff:

        if request.method == 'GET':
            username = request.user.username
            Image1 = friendvisitor.objects.filter(status='allow')
            Image1 = Image1.order_by('-id')
            stu1 = {"details": Image1}
            print (stu1)
            return render(request,'Request_staff.html',stu1)
        elif request.method == 'POST':
            if 'collected' in request.POST:
                team = friendvisitor.objects.filter(user=request.POST.get("student_name"))
                i=0
                for i in team:
	                if i.response == 'not collected' and i.status== 'allow':
	                    i.response = "collected"
	                i.save(update_fields=['response'])
	                i.save()
                return HttpResponse("added", content_type='text/plain')


    else:

	    username = request.user.username
	    Image2 = friendvisitor.objects.all()
	    Image2 = Image2.order_by('-id')
	    stu2 = {"details": Image2}
	    print (stu2)
	    return render(request,'Request_handling.html',stu2)


        #return render(request,'Request_handling.html',stu1)
    return HttpResponse("okay", content_type='text/plain')


@login_required
def urgent_request_status(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            Image = urgentvisitor.objects.all()
            Image = Image.order_by('-id')
            #print (Image)
            #print(type(Image))

            stu = {"details": Image }
            return render(request,'request_status.html',stu)
        if request.method == 'POST':
            if 'reject' in request.POST :
                team = urgentvisitor.objects.get(id=request.POST.get("student_id"))

                if team.status == 'allow':
                    team.status = 'pending'
                team.save(update_fields=['status'])
                team.save()

            elif 'accept' in request.POST :
                team = urgentvisitor.objects.get(id=request.POST.get("student_id"))
                if team.status == 'pending':
                    team.status = 'allow'
                team.save(update_fields=['status'])
                team.save()

            return HttpResponse("added", content_type='text/plain')


    elif  request.user.is_staff:

        if request.method =='GET':
            username = request.user.username
            Image1 = urgentvisitor.objects.filter(status='allow')
            Image1 = Image1.order_by('-id')
            stu1 = {"details": Image1}
            print (stu1)
            return render(request,'Request_staff.html',stu1)
        elif request.method == 'POST':
            if 'collected' in request.POST:
                team = urgentvisitor.objects.filter(user=request.POST.get("student_name"))
                i=0
                for i in team:
	                if i.response == 'not collected' and i.status== 'allow':
	                    i.response = "collected"
	                i.save(update_fields=['response'])
	                i.save()
                return HttpResponse("added", content_type='text/plain')
    else:

	    username = request.user.username
	    Image2 = urgentvisitor.objects.all()
	    Image2 = Image2.order_by('-id')
	    stu2 = {"details": Image2}
	    print (stu2)
	    return render(request,'Request_handling.html',stu2)


        #return render(request,'Request_handling.html',stu1)
    return HttpResponse("okay", content_type='text/plain')



@login_required
def user_logout(request):
    #User.objects.create_user('john', email='lennon@thebeatles.com', password='johnpassword', is_staff=True)#instance = expectedvisitor.objects.all()
    #instance.delete()
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def passvalidate(request):
        if request.method=="POST":
            username=request.POST.get("username")
            password=request.POST.get("password")

            user=authenticate(username=username,password=password)

            if user:
                print ("password validation is succesful")
                return HttpResponse("password validation is succesful", content_type='text/plain')

            else:
                print("invalid username and password")
                return HttpResponse("wrong credantials", content_type='text/plain')

        else :
            return render(request,'passvalidate.html',)



# Create your views here.
def user_login(request):
    if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
    else:
        if request.method=="POST":
            username=request.POST.get("username")
            password=request.POST.get("password")

            user=authenticate(username=username,password=password)

            if user:
                login(request,user)
                return HttpResponseRedirect(reverse('index',))
            else:
                return HttpResponse("invalid username and password")
        else :
            return render(request,'login.html',)


def authentication_view(request):
    registered = False

    if request.method=="POST":
        print(request.POST)
        auth=Authentic(request.POST )

        if auth.is_valid():
            auth=auth.save(commit=False)
            auth.set_password(auth.password)
            #hashing the password
            auth.save()
            registered=True
        else :
            print("error")
    else:
        auth=Authentic()
    return render(request,'login.html',)
