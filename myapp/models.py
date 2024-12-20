from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission
from django.core.exceptions import ValidationError

class User(AbstractUser):
    roles={
        ('user','User'),
        ('organiser','Organiser')
    }
    roll_no=models.CharField(max_length=9,unique=True,null=True,blank=True)
    role=models.CharField(max_length=10,choices=roles, default='user')
    name=models.CharField(max_length=100)


    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_group',  # Unique related_name
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='user_permissions_set',  # Unique related_name
        blank=True,
    )

    def clean(self):
        if self.role== 'user' and not self.roll_no:
            raise ValidationError("User requires a roll_no")
        if self.role=='organiser' and self.roll_no:
            raise ValidationError("Organiser does not have a roll_no")

    def __str__(self):
        return self.username


class Event(models.Model):
    
    venues=[
        ('OAT','OAT'),
        ('Auditorium','Auditorium',),
        ('Aryabhatta_Hall','Aryabhatta_Hall'),
        ('Bhaskara_Hall','Bhaskara_Hall'),
        ('Chanakya_Hall','Chanakya_Hall'),
        ('SOMS','SOMS')
    ]
    
    title= models.CharField(max_length=40,null=False,blank=False)
    description=models.TextField(max_length=10000,null=False,blank=False)
    date=models.DateField(null=False,blank=False)
    start_time=models.TimeField(null=False,blank=False)
    end_time=models.TimeField(null=False,blank=False)
    venue=models.CharField(max_length=100,choices=venues,null=False,blank=False)
    capacity=models.IntegerField()
    organiser=models.ForeignKey(User,on_delete=models.CASCADE)
    tags=models.JSONField(default=list)

    def __str__(self):
        return self.title
    
class Registration(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    event=models.ForeignKey(Event,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.roll_no} registered for {self.event.title}"