from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.urls import reverse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import reportlab

from django.db.models import Count, Q
from .models import Profile,Complaint

from django.shortcuts import get_object_or_404,render, redirect
from django.http import HttpResponse
from .forms import UserRegisterForm,ProfileUpdateForm,UserProfileform,ComplaintForm,UserProfileUpdateform,statusupdate,DocumentForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from datetime import datetime
from .models import Document


#page loading.
def index(request):
    return render(request,"GRsystem/home.html")

def my_view(request):
    Complaint(f"Great! You're using Python 3.6+. If you fail here, use the right version.")
    message = 'Upload as many files as you want!'
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return redirect('my-view')
        else:
            message = 'The form is not valid. Fix the following error:'
    else:
        form = DocumentForm()  # An empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    context = {'documents': documents, 'form': form, 'message': message}
    return render(request, 'GRsystem/list.html', context)

@login_required
def my_view2(request):
    Complaint(f"Great! You're using Python 3.6+. If you fail here, use the right version.")
    message = 'Upload as many files as you want!'
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return redirect('my-view2')
        else:
            message = 'The form is not valid. Fix the following error:'
    else:
        form = DocumentForm()  # An empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    context = {'documents': documents, 'form': form, 'message': message}
    return render(request, 'GRsystem/list.html', context)






def aboutus(request):
    return render(request,"GRsystem/aboutus.html")


def admin(request):
    return render(request,"GRsystem/signinadmin.html")

def login(request):
    return render(request,"GRsystem/login.html")

def signin(request):
    return render(request,"GRsystem/signin.html")

#get the count of all the submitted Complaints,solved,unsolved.
def counter(request):
        total=Complaint.objects.all().count()
        unsolved=Complaint.objects.all().exclude(status='1').count()
        solved=Complaint.objects.all().exclude(Q(status='3') | Q(status='2')).count()
        dataset=Complaint.objects.values('Type_of_Print').annotate(total=Count('status'),solved=Count('status', filter=Q(status='1')),
                  notsolved=Count('status', filter=Q(status='3')),inprogress=Count('status',filter=Q(status='2'))).order_by('Type_of_Print')
        args={'total':total,'unsolved':unsolved,'solved':solved,'dataset':dataset,}
        return render(request,"GRsystem/counter.html",args)


#registration page.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        profile_form=UserProfileform(request.POST)
        if form.is_valid() and profile_form.is_valid() :
            
            new_user=form.save()
            profile=profile_form.save(commit=False)
            if profile.user_id is None:
                profile.user_id=new_user.id
            profile.save()
            messages.add_message(request,messages.SUCCESS, f' Registered Successfully ')
            return redirect('/login/')
    else:
        form = UserRegisterForm()
        profile_form=UserProfileform()

    context={'form': form,'profile_form':profile_form }
    return render(request, 'GRsystem/register.html',context )

#login based on user.
def login_redirect(request):
    if request.user.profile.type_user=='student':
        return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/counter/')

@login_required
def dashboard(request):
        
    if request.method == 'POST':
        p_form=ProfileUpdateForm(request.POST,instance=request.user)
        profile_update_form=UserProfileUpdateform(request.POST,instance=request.user.profile)
        if p_form.is_valid() and profile_update_form.is_valid():
                user=p_form.save()
                profile=profile_update_form.save(commit=False)
                profile.user=user
                profile.save()
                messages.add_message(request,messages.SUCCESS, f'Update Successfully Done')
                return render(request,'GRsystem/dashboard.html',)
    else:
        p_form=ProfileUpdateForm(instance=request.user)
        profile_update_form=UserProfileUpdateform(instance=request.user.profile)
    context={
        'p_form':p_form,
        'profile_update_form':profile_update_form
        }
    return render(request, 'GRsystem/dashboard.html',context)

#change password for user.

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) 
            messages.add_message(request,messages.SUCCESS, f'Your NCI password was successfully updated!')
            return redirect('change_password')
        else:
            messages.add_message(request,messages.WARNING, f'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'GRsystem/change_password.html', {
        'form': form
    })


def change_passwords(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) 
            messages.add_message(request,messages.SUCCESS, f'Your NCI password was successfully updated!')
            return redirect('change_password')
        else:
            messages.add_message(request,messages.WARNING, f'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'GRsystem/change_password.html', {
        'form': form
    })





#Complaints handling and submission section.
@login_required
def Complaints(request):
  
    if request.method == 'POST':
           
        
        Complaint_form=ComplaintForm(request.POST)
        if Complaint_form.is_valid():
            
          
               savetheComplaint=Complaint_form.save(commit=False)
               savetheComplaint.user=request.user
               savetheComplaint.save()
               
               messages.add_message(request,messages.SUCCESS, f'NCI Prints has received your Complaint.We will get back to you Soon!!!')
               return render(request,'GRsystem/comptotal.html',)
    else:
        
        Complaint_form=ComplaintForm(request.POST)
    context={'Complaint_form':Complaint_form,}
    return render(request,'Grsystem/comptotal.html',context)
        

@login_required
def list(request):
    c=Complaint.objects.filter(user=request.user).exclude(status='1')
    result=Complaint.objects.filter(user=request.user).exclude(Q(status='3') | Q(status='2'))
    #c=Complaint.objects.all()
    args={'c':c,'result':result}
    return render(request,'Grsystem/Complaints.html',args)
@login_required
def slist(request):
    result=Complaint.objects.filter(user=request.user).exclude(Q(status='3') | Q(status='2'))
    #c=Complaint.objects.all()
    args={'result':result}
    return render(request,'Grsystem/solvedComplaint.html',args)

@login_required
def allprintrequests(request):
      
        
        c=Complaint.objects.all().exclude(status='1')
        comp=request.GET.get("search")
        drop=request.GET.get("drop")

        if drop:
                c=c.filter(Q(Type_of_Print__icontains=drop))
        if comp:
                c=c.filter(Q(Type_of_Print__icontains=comp)|Q(Address__icontains=comp)|Q(Subject__icontains=comp))
        if request.method=='POST':
                cid=request.POST.get('cid2')
                uid=request.POST.get('uid')
                Complaint(uid)
                project = Complaint.objects.get(id=cid)
                
                forms=statusupdate(request.POST,instance=project)
                if forms.is_valid():
                        
                        obj=forms.save(commit=False)
                        obj.save()
                        messages.add_message(request,messages.SUCCESS, f'Complaint Updated!!!')
                        return HttpResponseRedirect(reverse('allprintrequests'))
                else:
                        return render(request,'GRsystem/allprintrequests.html')
        

        else:
                forms=statusupdate()
                   
        args={'c':c,'forms':forms,'comp':comp}
        return render(request,'Grsystem/allprintrequests.html',args)

@login_required
def solved(request):
        
        cid=request.POST.get('cid2')
        c=Complaint.objects.all().exclude(Q(status='3') | Q(status='2'))
        comp=request.GET.get("search")
        drop=request.GET.get("drop")

        if drop:
                c=c.filter(Q(Type_of_Print__icontains=drop))
        if comp:
               
                c=c.filter(Q(Type_of_Print__icontains=comp)|Q(Address__icontains=comp)|Q(Subject__icontains=comp))
        if request.method=='POST':
                cid=request.POST.get('cid2')
                Complaint(cid)
                project = Complaint.objects.get(id=cid)
                forms=statusupdate(request.POST,instance=project)
                if forms.is_valid():
                        
                        obj=forms.save(commit=False)
                        obj.save()
                        messages.add_message(request,messages.SUCCESS, f'Complaint Updated!!!')
                        return HttpResponseRedirect(reverse('solved'))
                else:
                        return render(request,'GRsystem/solved.html')
                 #testing

        else:
                forms=statusupdate()
        
        args={'c':c,'forms':forms,'comp':comp}
        return render(request,'Grsystem/solved.html',args)

#allprintrequests pdf viewer.
def pdf_viewer(request):
    detail_string={}
    #detailname={}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Suhail-x20191065.pdf'
    p = canvas.Canvas(response,pagesize=A4)
    
    cid=request.POST.get('cid')
    uid=request.POST.get('uid')
    #Complaint(cid)
    
    details = Complaint.objects.filter(id=cid).values('Address')
    
    name = Complaint.objects.filter(id=cid).values('user_id')
    Subject = Complaint.objects.filter(id=cid).values('Subject')
    Type = Complaint.objects.filter(id=cid).values('Type_of_Print')
    Issuedate = Complaint.objects.filter(id=cid).values('Time')
    #date_format1 = "%Y-%m-%d %H:%M:%S.%f%z"
   
    
    for val in details:
            detail_string=("{}".format(val['Address']))
    for val in name:
           detailname=("User: {}".format(val['user_id']))
    
    for val in Subject:
            detailsubject=("Subject: {}".format(val['Subject']))
    for val in Type:
            detailtype=("{}".format(val['Type_of_Print']))
            
    for val in Issuedate:
            ptime=("{}".format(val['Time']))
            detailtime=("Time of Issue/ Time of Solved: {}".format(val['Time']))
    date_format = "%Y-%m-%d"
    a = datetime.strptime(str(datetime.now().date()), date_format)
    b = datetime.strptime(str(ptime), date_format)
    delta = a - b
    Complaint(b)
    Complaint(a)
    Complaint (delta.days )       
    if detailtype=='1':
            detailtype="Type of Complaint: ClassRoom"
    if detailtype=='3':
            detailtype="Type of Complaint: Management"
    if detailtype=='2':
            detailtype="Type of Complaint: Teacher"
    if detailtype=='4':
            detailtype="Type of Complaint: School"
    if detailtype=='5':
            detailtype="Type of Complaint: Other"

    p.drawString(25, 770,"Report:")
    p.drawString(30, 750,detailname)
    ''' p.drawString(30, 730,detailbranch)'''
    p.drawString(30, 710,detailtype)
    p.drawString(30, 690,detailtime)
    p.drawString(30, 670,detailsubject)
    p.drawString(30, 650,"Address:")
    p.drawString(30, 630,detail_string)

    p.showPage()
    p.save()
    return response

#Complaints pdf view.
@login_required
def pdf_view(request):
    detail_string={}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Complaint_id.pdf'
    
    p = canvas.Canvas(response,pagesize=A4)
    cid=request.POST.get('cid')
    
    details = Complaint.objects.filter(id=cid).values('Address')
    name = User.objects.filter(username=request.user.username).values('username')
    
    Subject = Complaint.objects.filter(id=cid).values('Subject')
    Type = Complaint.objects.filter(id=cid).values('Type_of_Print')
    Issuedate = Complaint.objects.filter(id=cid).values('Time')

    for val in details:
            detail_string=("{}".format(val['Address']))
    for val in name:
            detailname=("User: {}".format(val['username']))
    for val in Subject:
            detailsubject=("Subject: {}".format(val['Subject']))
    for val in Type:
            detailtype=("{}".format(val['Type_of_Print']))
            
    for val in Issuedate:
            detailtime=("Time of Issue: {}".format(val['Time']))
    if detailtype=='1':
            detailtype="Type of Complaint: ClassRoom"
    if detailtype=='3':
            detailtype="Type of Complaint: Management"
    if detailtype=='2':
            detailtype="Type of Complaint: Teacher"
    if detailtype=='4':
            detailtype="Type of Complaint: School"
    if detailtype=='5':
            detailtype="Type of Complaint: Other"

    p.drawString(25, 770,"Report:")
    p.drawString(30, 750,detailname)
    p.drawString(30, 710,detailtype)
    p.drawString(30, 690,detailtime)
    p.drawString(30, 670,detailsubject)
    p.drawString(30, 650,"Address:")
    p.drawString(30, 630,detail_string)

    p.showPage()
    p.save()
    return response




             

