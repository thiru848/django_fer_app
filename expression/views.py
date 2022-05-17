from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMessage, send_mail
from django.contrib.sites.shortcuts import get_current_site

from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator

import random
import time
from recognition import settings
from . tokens import generate_token
from . models import Song
from datetime import date


# USER Model
User = get_user_model()

# Create your views here.
def home(request):
    return render(request, 'expression/index.html')

def about(request):
    return render(request, 'expression/about.html')

def faq(request):
    return render(request, 'expression/faq.html')

def signup(request):
    if request.method == "POST":
        
        fname = request.POST['fname']
        lname = request.POST['lname']
        utype = request.POST['utype']
        dob = request.POST['dob']
        phone = request.POST['phone']
        email = request.POST['email']
        #street = request.POST['address']
        #city = request.POST['city']
        #state = request.POST['state']
        #country = request.POST['country']
        #pincode = request.POST['pincode'] 
        user_name = request.POST['username']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(user_name=user_name):
            messages.error(
                request, "User name already exists! Please try some other username")
            return redirect('signin')

        if User.objects.filter(email=email):
            messages.error(request, "Email already registered!")
            return redirect('signin')

        if len(user_name) > 15:
            messages.error(request, "Username must be under 15 characters!")
            return redirect('signin')

        if pass1 != pass2:
            messages.error(request, "Passowords didn't match!")
            return redirect('signin')

        if not user_name.isalnum():
            messages.error(request, "Username must be alpha numeric")
            return redirect('signin')
        
        myuser = User.objects.create_user(email, user_name, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_doctor = True if utype == 'Doctor' else False
        myuser.dob = dob
        myuser.phone = phone
        #myuser.street = street
        #myuser.city = city
        #myuser.state = state
        #myuser.country = country
        #myuser.pincode = pincode
        myuser.is_active = False

        myuser.save()
        messages.success(request, "Your account has been sucessfully created. We have sent you a confirmation mail, please confirm your email in order to activate your account.")

        # Welcome mail
        subject = "Welcome to ASTS - Psychology Login!!"
        message = "Hello " + myuser.first_name + " !!\nWelcome to ASTS!! \n Thank you for visiting our website.\n" \
            "We have also sent you a confirmation mail, please confirm your email address in order to activate your account.\n" \
            "\n Thanking You\n Admin"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]

        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # Confirmation mail
        current_site = get_current_site(request)
        email_subject = "Confirm your email @ ASTS - Psychology Login!!"
        message2 = render_to_string('email_confirmation.html', {
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email]
        )
        email.fail_silently = True
        email.send()

        return redirect('signin')

    return render(request, 'expression/signup.html')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('signin')
    else:
        messages.error(request, "Activation failed, please try again!")
        return redirect('signin')

def signin(request):
    if request.method == "POST":
        user_name = request.POST['username']
        password = request.POST['password']

        user = authenticate(user_name=user_name, password=password)

        if user is None: 
            messages.error(request, "Bad Credentials.")
            return redirect('signin')
        elif not user.is_active:
            messages.error(request, "First activate your account by link sended to your mail!")
        else:
            login(request, user)
            return redirect('dashboard')

    return render(request, 'expression/login.html')

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('signin')

def forgot(request):
    if request.method == "POST":
        email = request.POST['email']
        user = User.objects.get(email=email)
        if user is not None:
            user_name = user.user_name
            fname = user.first_name
            user.otp = int(''.join(random.choices('1234567890', k = int(''.join(random.choices('456', k=1))))))
            user.save()

            from_email = settings.EMAIL_HOST_USER
            subject = 'OTP generated for Forgot Password'
            message = 'Hello '+fname+',\n\n'+' OTP :  '+str(user.otp)+'\n\nThanks'
            to_list = [email]

            send_mail(subject, message, from_email, to_list, fail_silently=True)
            messages.success(request, 'OTP generated check your mail!!')
            
            return render(request, 'expression/forgotpassword.html', {'username':user_name})
        else:
            messages.error(request, 'Please use the Registered email!')
    
    return render(request, 'expression/forgotpassEmail.html')

def callotp(request):
    if request.method == "POST":
        otp = request.POST['otp']
        user_name = request.POST['username']
        user = User.objects.get(user_name=user_name)
        if(user.otp == int(otp)):
            messages.success(request, 'Change the password as you wish!!')
            time.sleep(2)
            return render(request, 'expression/newpass.html', {'username':user_name})
        else:
            messages.error(request, 'Required the correct otp!')
    
    return render(request, 'expression/forgotpassword.html')

def verify(request):
    if request.method == "POST":
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        if pass1 == pass2:
            user_name = request.POST['username']
            user = User.objects.get(user_name=user_name)
            user.set_password(pass1)
            user.save()

            messages.success(request, 'Updated the new password!!')
            time.sleep(2)
            return redirect('signin')
        else:
            messages.error(request, "Passowords didn't match!")

    return render(request, 'expression/newpass.html')

def dashboard(request):
    user = User.objects.get(user_name = request.user.user_name)
    context = {'user_name':user.user_name, 'is_doctor':user.is_doctor}
    return render(request, 'expression/dashboard.html', context)

def profile(request):
    user = User.objects.get(user_name = request.user.user_name)
    context = {'user_name':user.user_name, 'fname':user.first_name, 'lname':user.last_name, 
                'age':calcAge(user.dob), 'phone':user.phone, 'email':user.email}
    return render(request, 'expression/profile.html', context)

def reset(request):
    if request.method == "POST":
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        pass3 = request.POST['pass3']

        user = User.objects.get(user_name = request.user.user_name)
        if user.check_password(pass1):
            if pass2 == pass3:
                user.set_password(pass2)
                user.save()
                login(request, user)

                messages.success(request, "Reseted the password successfully!")
                time.sleep(2)

                context = {'user_name':user.user_name, 'fname':user.first_name, 'lname':user.last_name, 
                'age':calcAge(user.dob), 'phone':user.phone, 'email':user.email}

                return render(request,'expression/profile.html', context)
            else:
                messages.error(request, "Passwords didn't match!")
                time.sleep(2)
        else:
            messages.error(request, "Enter the current password correctly!")
            time.sleep(2)
        
        return render(request,'expression/resetpassword.html')
    
    return render(request,'expression/resetpassword.html')

def music(request):
    paginator = Paginator(Song.objects.all(),1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {"page_obj":page_obj}
    return render(request, 'expression/music.html', context)

def report(request):
    user = User.objects.get(user_name = request.user.user_name)
    context = {'user_name':user.user_name, 'fname':user.first_name, 'lname':user.last_name, 
                'age':calcAge(user.dob), 'phone':user.phone, 'email':user.email}
    return render(request, 'expression/report.html', context)

def calcAge(dob):
    today = date.today()
    try:
        birth = dob.replace(year=today.year)
    except ValueError: # raised when birth date is Feb 29 & current year is not lep year
        birth = dob.replace(year=today.year, month=dob.month+1, day=1)
    if birth > today:
        return today.year - dob.year - 1
    else:
        return today.year - dob.year

