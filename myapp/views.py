from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import *
from .serializers import *

from rest_framework.response import Response
from rest_framework.views import APIView


from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework import generics
# Create your views here.
from django.contrib.auth import authenticate

from rest_framework_simplejwt.authentication import JWTAuthentication

class UserRegistration(APIView):

    def post(self,request):
        serializer=UserSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({'status':403,"message":"Invalid Details"})

        serializer.save()
        username=request.data.get('roll_no')
        user=User.objects.get(username=username)
        refresh= RefreshToken.for_user(user)

        return Response({'status':200, 'payload':serializer.data,'refresh':str(refresh),'access':str(refresh.access_token),'message':"User Registered Succesfully"})

class Login(APIView):

    def post(self,request):
        password=request.data.get('password')
        username = request.data.get('roll_no') or request.data.get('name') or request.data.get('username')
        print(f"{username} {password}")
        user = authenticate(username=username, password=password)
        print(user.username)
        if user is None:
            return Response({'status': 401, 'message': "Invalid Credentials"})
        refresh = RefreshToken.for_user(user)
        return Response({'status': 200, 'payload': user.username, 'refresh': str(refresh), 'access': str(refresh.access_token), 'message': "Logged in successfully"})

from rest_framework.permissions import BasePermission, IsAuthenticated,IsAdminUser

class IsAdminorOrganiser(BasePermission):
    def has_permission(self, request, view):
        
        return  request.user.is_authenticated and (request.user.role=='organiser' or request.user.is_staff)

class IsUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role=='user'
    

class IsAdminorEventOrganiser(BasePermission):
    def has_object_permission(self, request, view,obj):
        return request.user.is_authenticated and (obj.organiser== request.user or request.user.is_staff)

class IsAdminorEventOrganiserorSameUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (obj.organiser== request.user or request.user.is_staff or obj.user==request.user)
    

class CreateOrganiser(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAdminUser]

    def post(self,request):
        serializer=UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'status':200,'message':"Invalid Detatils"})
        serializer.validated_data['role']='organiser'
        organiser=serializer.save()
        return Response({'status':200,'message':f'Organiser {organiser.name} has been created'})

class CreateEvent(APIView):

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAdminorOrganiser]

    def post(self,request):

        data=request.data.copy()
        data['organiser']=request.user.id
        serializer=EventSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({"status": 200,  "data": serializer.data, "message": "Event created successfully"})
        return Response({"status": 400, "message": "Event creation failed"})

class UpdateEvent(generics.DestroyAPIView,generics.RetrieveAPIView,generics.UpdateAPIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAdminorEventOrganiser]

    queryset=Event.objects.all()
    serializer_class=EventDetailsSerializer
    lookup_field='id'

class GetAllEvents(generics.ListAPIView):
    queryset=Event.objects.all().order_by('date','venue','start_time')
    serializer_class=EventSerializer


from rest_framework.exceptions import ValidationError

class RegisterforEvent(APIView):

    authentication_classes=[JWTAuthentication]
    permission_classes=[IsUser]
    
    def post(self,request,id):
        user=request.user
        if not user:
            return Response({'status': 400, 'message': "Invalid user instance."})
        
        event=Event.objects.get(id=id)
        if not event:   
            return Response({'status':404,'message':"Event not found"})
        
        if Registration.objects.filter(user=user,event=event).exists():
            raise ValidationError("You are already registered for this event.")
        
        if Registration.objects.filter(event=event).count()>=event.capacity:
            return Response({'status':400, 'message':"Event already at full capacity"})

        Registration.objects.create(user=user, event=event)
        return Response({'status':200,'message':f"You have succesfully Registered for {event.title}"})

class Unregister(generics.DestroyAPIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsUser]

    def delete(self,request,id):
        event=Event.objects.get(id=id)
        if not event:
            return Response({'status':404,'message':"Event not found"})

        registration = Registration.objects.filter(user=request.user, event=event)

        if not registration.exists():
            raise ValidationError("You have not registered for this event.")
        
        registration.delete()
        return Response({'status':200,'message':f"You have succesfully Unregistered for {event.title}"})

    