from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

from django.core.validators import RegexValidator
from datetime import datetime

class Meta:

    app_label = 'GRsystem'
class Profile(models.Model):
    typeuser =(('student','student'),('grievance', 'grievance'))
    COL=(('Technical','Technical'),('Business','Business')) 
    user =models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    collegename=models.CharField(max_length=29,choices=COL,blank=False)
    phone_regex =RegexValidator(regex=r'^\d{10,10}$', message="Phone number must be entered in the format:Up to 10 digits allowed.")
    contactnumber = models.CharField(validators=[phone_regex], max_length=10, blank=True) 
    type_user=models.CharField(max_length=20,default='student',choices=typeuser)
    CB=(('Cloud Computing',"Cloud Computing"),('Cyber Security',"Cyber Security"),('DA Group A',"DA Group A"),('DA Group B',"DA Group B"))
    Branch=models.CharField(choices=CB,max_length=29,default='Technical')
    def __str__(self):
        return self.collegename
    def __str__(self):
        return self.user.username
    
from django.db import models


class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class Complaint(models.Model):
    STATUS =((1,'Solved'),(2, 'InProgress'),(3,'Pending'))
    TYPE=(('Colour-A4',"Colour-A4"),('Colour-A3',"Colour-A3"),('Black and White-A4',"Black and White-A4"),('Black and White-A3',"Black and White-A3"),('Other-Please mention in the Address box',"Other-Please mention in the Address box"))
    
    Subject=models.CharField(max_length=200,blank=False,null=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE,default=None)
    
    Type_of_Print=models.CharField(choices=TYPE,null=True,max_length=200)
    Address=models.TextField(max_length=4000,blank=False,null=True)
    
    Time = models.DateField(auto_now=True)
    status=models.IntegerField(choices=STATUS,default=3)
    
   
    def __init__(self, *args, **kwargs):
        super(Complaint, self).__init__(*args, **kwargs)
        self.__status = self.status

    def save(self, *args, **kwargs):
        if self.status and not self.__status:
            self.active_from = datetime.now()
        super(Complaint, self).save(*args, **kwargs)
    
    def __str__(self):
     	return self.get_Type_of_Print_display()
def __str__(self):
        return str(self.user)

class Grievance(models.Model):
    guser=models.OneToOneField(User,on_delete=models.CASCADE,default=None)

    def __str__(self):
        return self.guser