from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate, login 
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
import pyotp 
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .speech import transcribe_speech, translate_text, transliterate_text
from django.http import JsonResponse
from .speech import get_supported_languages
from .models import Feedback

@csrf_protect
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        confirm_password = request.POST['password2']

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, 'Signup successful! Redirecting to login page.')
        return redirect('login')
    return render(request, 'signup.html')

def signin(request):
    if request.method=="POST":
        name=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=name,password=password)
        
        if user is not None:
            login(request,user)
            return render(request,"trans.html")
        else:
            messages.success(request,"Invalid username / password ")
            return render(request,"login.html")
    if not request.user.is_anonymous:
         return render(request,"trans.html")   
    return render(request,"login.html")

#def logout(request):
    return render(request,'logout.html')

def home(request):
    return render(request,'home.html')

def send_otp_email(request,email):
    # Generate a new OTP
    otp_secret = pyotp.random_base32()
    otp = pyotp.TOTP(otp_secret)
    otp_code = otp.now()

    # Send the OTP via email
    subject = 'OTP Verification'
    message = f'Your OTP code is: {otp_code}'
    from_email = settings.EMAIL_HOST_USER   # Replace with your email
    recipient_list = [email]
    request.session['otp']=otp_code
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

    # Store the OTP secret key temporarily (e.g., in session or database)
    return otp_secret

def send_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user=User.objects.filter(username=email)
        if user:
            return redirect('/everify')
        otp_secret = send_otp_email(request,email)

        # Store the OTP secret key in the session (or database) for later verification
        request.session['otp_secret'] = otp_secret
        request.session['email'] = email

        return redirect('verify_otp')

    return redirect('login')

def verify_otp(request):
    if request.method == 'POST':
        otp_code = request.POST.get('otp')
        print(otp_code)
        print(request.session['otp'])
        otp_secret = request.session.get('otp_secret')

        if not otp_secret:
            # Handle the case where the OTP secret key is not available
            return redirect('send_otp')

        if otp_code==request.session['otp']:
            # Mark the email as verified in your database
            print("OTP verification successful")
            
            del request.session['otp_secret']
            del request.session['otp']
            
            return redirect('signup')  # Redirect to a success page
        else:
            print("OTP verification failed")
            
            return redirect('emailverify')

    return render(request, 'otp.html')




def about(request):
    return render(request,'about.html')

def trans(request):
    return render(request,'trans.html')
def logout_view(request):
    logout(request)
    return redirect('/login')  # Redirect to login page after logout
def emailverify(request):
    return render(request,'emailverify.html')

#def otp(request):
 #   return redirect('signup.html')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        # Add logic to generate and send OTP to the provided email
        send_mail(
            'Your OTP Code',
            'Here is your OTP code.',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        return redirect('otp_sent')
    return render(request, 'forgot_password.html')

def confirm_pass(request):
    return render(request,'confirm_pass.html')

@csrf_exempt
def process_speech(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        language = data.get('language')
        action = data.get('action')
        target_language = data.get('targetLanguage')
        transcription = data.get('transcription')

        if action == 'translate':
            translated_text = translate_text(transcription, language, target_language)
            return JsonResponse(translated_text, safe=False)
        elif action == 'transliterate':
            transliterated_text = transliterate_text(transcription, language, target_language)
            return JsonResponse(transliterated_text, safe=False)
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)

    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    
def get_supported_languages_view(request):
    supported_languages = get_supported_languages()
    return JsonResponse({"languages": supported_languages})   

def feedback(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['feedback']

        feedback_entry = Feedback(name=name, email=email, message=message)
        feedback_entry.save()
        return redirect('feedback')  # You can change this to a different URL if needed
    return render(request, 'feedback.html')

def send_otp2(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user=User.objects.filter(username=email)
        if user:
            return redirect('/everify')
        otp_secret = send_otp_email(request,email)

        # Store the OTP secret key in the session (or database) for later verification
        request.session['otp_secret'] = otp_secret
        request.session['email'] = email

        return redirect('verify_otp2')

    return redirect('login')

def verify_otp2(request):
    if request.method == 'POST':
        otp_code = request.POST.get('otp')
        print(otp_code)
        print(request.session['otp'])
        otp_secret = request.session.get('otp_secret')

        if not otp_secret:
            # Handle the case where the OTP secret key is not available
            return redirect('send_otp')

        if otp_code==request.session['otp']:
            # Mark the email as verified in your database
            print("OTP verification successful")
            
            del request.session['otp_secret']
            del request.session['otp']
            
            return redirect('confirm_pass')  # Redirect to a success page
        else:
            print("OTP verification failed")
            
            return redirect('forgot_password')
    return render(request, 'otp2.html')

from django.contrib.auth.models import User

# Function to reset password
def reset(request):
    if request.method == 'POST':
        username = request.POST['username']
        new_password = request.POST['new_password']
        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            messages.success(request, f"Password reset successful for user: {username}")
        except User.DoesNotExist:
            messages.error(request, f"User with username {username} does not exist.")
        return redirect('login')

    return render(request, 'reset.html')
