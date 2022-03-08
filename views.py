from email import message
from telnetlib import STATUS
from django.shortcuts import redirect, render
from django.template import context
from django.views import View
import json
from django.http import JsonResponse, request
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import reverse
from .utils import account_activation_token 
from django.contrib import auth


# Create your views here.
from validate_email import validate_email #type:ignore
class EmailValidationView(View):
    def post(self,request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
           return JsonResponse({'email_error':'Envalid Email'},status=400)

       # if User.objects.filter(email=email).exists():
          #  return JsonResponse({'email_error':'Sorry!! email already in use please choose other'},status=400)

        return JsonResponse({'email_valid':True})

class UsernameValidationView(View):
    def post(self,request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
           return JsonResponse({'username_error':'username contain only alphanumeric character'},status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error':'sorry!! username already in use please choose other'},status=400)

        return JsonResponse({'username_valid':True})

class RegistrationView(View):
    def get(self,request):
        return render(request,'authentication/register.html')

    def post(self,request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        context = {
            'fieldValues':request.POST
        }
    
        if not User.objects.filter(username=username).exists():
           #if not User.objects.filter(email=email).exists():
               
               if len(password) < 6:
                   messages.error(request,'password is too short!')
                   return render(request,'authentication/register.html',context)
               user = User.objects.create_user(username=username,email=email)
               user.set_password(password)
               user.is_active = False
               user.save()
               
               #for email verification and send link in email
               uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
               domain = get_current_site(request).domain
               link = reverse('activate',kwargs={'uidb64':uidb64,'token':account_activation_token.make_token(user)})
             
               activate_url= 'http://'+domain+link
               email_subject='Activat for account'
               email_body= 'Hi '+user.username + ', Please the link below to activate your account \n'+activate_url
               email = EmailMessage(
                 email_subject,
                 email_body,
                 'noreply@semycolon.com',
                 [email],
               )
               email.send(fail_silently=False)
               messages.success(request,'Register successfull')
               return render(request,'authentication/register.html')
        
        return render(request,'authentication/register.html')
    
class VerificationView(View):
    def get(self,request,uidb64,token):

         try:
             id = force_text(urlsafe_base64_decode(uidb64))
             user = User.objects.get(pk=id)

             if not account_activation_token.check_token(user, token):
                return redirect('login'+'?messages='+'User already activated')

             if user.is_active:
                return redirect('login')
             user.is_active=True
             user.save()
             messages.success(request,'account activated successfully')
             return redirect('login')

         except Exception as ex:
             pass
         return redirect('login')
class LoginView(View):
    def get(self,request):
         return render(request,'authentication/login.html')    

    def post(self,request):
        username = request.POST['username']   
        password = request.POST['password']   

        if username and password:
            user = auth.authenticate(username=username,password=password)

            if user:
                if user.is_active:
                    auth.login(request,user)
                    messages.success(request,'Welcome! '+ user.username +' you are logged in')
                    return redirect('expenses')
                messages.error(request,'Account is not active,please check your email')
                return render(request,'authentication/login.html')    
            messages.error(request,'Wrong credentials try again!')
            return render(request,'authentication/login.html')    
        messages.error(request,'Please fill all fields!')
        return render(request,'authentication/login.html')    

class LogoutView(View):
    def post(self,request):
        auth.logout(request)
        messages.success(request,'you have been logout')
        return redirect('login')

def profile_edit(request,id):
    user=User.objects.get(pk=id)

    context={
     'user':user,
     'values':user
    }
    if request.method=='GET':
        return render(request,'authentication/edit-profile.html',context)
      
    if request.method=='POST':
        username = request.POST['username']

        if not username:
            messages.error(request,'username is required')
            return render(request, 'authentication/edit-profile.html',context)
       
        email = request.POST['email']
        Id = request.POST['id']
        
        if not Id:
            messages.error(request,'Id is required')
            return render(request, 'authentication/edit-profile.html',context)
       

        if not email:
            messages.error(request,'Email is required')
            return render(request, 'authentication/edit-profile.html',context)
        
        user.owner=request.user
        user.username=username
        user.email=email
        user.id=Id
        
        user.save()
        messages.success(request,'Profile updated successfully')
        return redirect('profile')
  
def profile_view(request):
    context = {

    }
    return render(request, 'authentication/edit-profile.html', context)