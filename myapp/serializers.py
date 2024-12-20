from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['name','roll_no','password']
        extra_kwargs={
            'password':{'write_only':True},
        }
    
    def create(self, validated_data):
        password=validated_data.pop('password')
        user=User(**validated_data)
        
        if validated_data.get('roll_no') :
            user.username=validated_data.get('roll_no') 
        else:

            user.username=validated_data.get('name')
        user.set_password(password)
        user.save()
        return user

from rest_framework.exceptions import ValidationError

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model=Event
        fields='__all__'

    def create(self, validated_data):
        start=validated_data['start_time']
        end=validated_data['end_time']
        date=validated_data['date']
        venue=validated_data['venue']
        
        if end<=start:
            raise ValidationError("Start time cannot be greater than or equal to end time")

        overlap=Event.objects.filter(
            date=date,
            venue=venue,
            start_time__lt=end, # Existing event starts before the new event ends
            end_time__gt=start  # Existing event ends after the new event starts
        )

        if overlap.exists():
            raise ValidationError("There is already an event scheduled here")
        event=super().create(validated_data)
        return event
        # schedule=Event.objects.filter(date=date,venue=venue).order_by('start_time')

        # if not schedule:
        #     event=Event(**validated_data)
        #     event.save()
        #     return event
        # prev_sched=None

        # for sched in schedule:
        #     if end<=sched.start_time:

        #         if prev_sched is None or start>=prev_sched.end_time:
        #             event=Event(**validated_data)
        #             event.save()
        #             return event
        #     prev_sched=sched
        
        # if start>=prev_sched.end_time:
        #     event=Event(**validated_data)
        #     event.save()
        #     return event
        
class EventDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Event
        fields='__all__'

    def get_registrations(self,obj):
        registrations=Registration.objects.filter(event=obj).select_related('user')   
        return[
            {
                'Roll_no':reg.user.roll_no,
                'name':reg.user.roll_no
            }for reg in registrations
        ] 

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Registration
        fields='__all__'
