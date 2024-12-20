from django.urls import path
from .views import *

urlpatterns=[
    path('userregister',UserRegistration.as_view(),name='UserRegistration'),
    path('login',Login.as_view(),name='Login'),
    path('createorganiser',CreateOrganiser.as_view(),name='CreateOrganiser'),

    path('api/events/create',CreateEvent.as_view(),name='CreateEvent'),
    path('api/events/all',GetAllEvents.as_view(),name='GetAllEvents'),
    
    path('api/events/<int:id>',UpdateEvent.as_view(),name='UpdateEvent'),

    path('api/events/register/<int:id>',RegisterforEvent.as_view(),name='RegisterforEvent'),
    path('api/events/unregister/<int:id>',Unregister.as_view(),name='Unregister'),
]