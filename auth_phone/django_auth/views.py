from django.shortcuts import render,redirect

# Create your views here.

from django.conf import settings
from django.contrib.auth import get_user_model
from twilio.rest import Client
from django.contrib.auth import login,logout,authenticate
from django.views import View
from .models import PhoneOTP
from .forms import PhoneNumberForm,OTPForm
from django.db import IntegrityError
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from twilio.base.exceptions import TwilioRestException

import random

User = get_user_model()

client = Client(settings.TWILIO_ACCOUNT_SID,settings.TWILIO_AUTH_TOKEN)

def register(request):

    if request.method == 'POST':

        first_name = request.POST.get('f_name')
        last_name = request.POST.get('l_name')
        phone_number = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not phone_number.startswith('+'):
                phone_number = '+91' + phone_number

        user= User.objects.filter(phone_number=phone_number)

        if user.exists():
            messages.info(request,'Phone number already exists')

            return redirect('/register/')
        
        try:
            user=User.objects.create(
                first_name = first_name,
                last_name = last_name,
                phone_number = phone_number,
                email = email,
                password = password,
            )

            user.set_password(password)
            user.save()

            messages.info(request,'Successfully register')
            return redirect('/login/')
        
        except IntegrityError:
            messages.error(request,'An error occurred')
            return redirect('/register/')


    return render(request,'register.html')

class LoginView(View):
    template_name_phone = 'login.html'
    template_name_otp = 'otp.html'
    OTP_VALIDITY_PERIOD = timedelta(minutes=5) 

    def get(self, request):
        form = PhoneNumberForm()
        
        return render(request, self.template_name_phone, {'form': form})

    def post(self, request):
        phone_form = PhoneNumberForm(request.POST)
        otp_form = OTPForm(request.POST)

        if 'phone_number' in request.POST and phone_form.is_valid():
            phone_number = phone_form.cleaned_data['phone_number']
            
            if not phone_number.startswith('+'):
                phone_number = '+91' + phone_number
            
            
            
            # Check if user with the phone number alreadify exists
            if not User.objects.filter(phone_number=phone_number).exists():

                messages.error(request, 'Phone number not registered. Please register first.')
                return redirect('/register/')


            otp = str(random.randint(100000, 999999))

            now = timezone.now()
            # Check for existing OTP records
            otp_record = PhoneOTP.objects.filter(phone_number=phone_number, validated=False, created_at__gt=now - self.OTP_VALIDITY_PERIOD).first()

            if otp_record:
                 messages.info(request, 'OTP has already been sent. Please check your phone.')
            else:

                # Create or update OTP record
                PhoneOTP.objects.update_or_create(
                phone_number=phone_number,
                defaults={'otp': otp, 'validated': False, 'created_at': now}
                )
                print(phone_number)
                print(otp)
                # Send OTP via Twilio
                try:
                    # Send OTP via Twilio
                    client.messages.create(
                        body=f'Your OTP is {otp}',
                        from_=settings.TWILIO_PHONE_NUMBER,
                        to=phone_number
                    )
                    messages.success(request, 'OTP sent successfully! Please check your phone.')
                    return render(request, self.template_name_otp, {'form':OTPForm(),'phone_number': phone_number})
                except TwilioRestException as e:
                    messages.error(request, f'Error sending OTP: {e.msg}')
                    return render(request, self.template_name_phone, {'form': phone_form})
           
        
        if 'otp' in request.POST and otp_form.is_valid():
            otp = otp_form.cleaned_data['otp']
            print(otp)
            phone_number = request.POST.get('phone_number')
            print(phone_number)
            phone_otp = PhoneOTP.objects.filter(phone_number=phone_number, otp=otp, validated=False , created_at__gt=timezone.now() - self.OTP_VALIDITY_PERIOD).first()

            if phone_otp:
                phone_otp.validated = True
                phone_otp.save()
                messages.success(request, 'Phone number verified successfully!')
                # Redirect to home or profile page after verification
                return redirect('/index/')  
            else:
                messages.error(request, 'Invalid OTP!')
                return render(request, self.template_name_otp, {'form': otp_form, 'phone_number': phone_number})

        return render(request, self.template_name_phone, {'form': phone_form})

def home(request):

    return render(request,'home.html')
def Logout(request):

    logout(request)

    return redirect('/login/')