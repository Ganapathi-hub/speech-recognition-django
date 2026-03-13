from django.contrib import admin
from django.urls import path
from home import views 
from . import views
from .views import process_speech
urlpatterns = [
    path('',views.home,name="home" ),
    path("login",views.signin, name='login'),
    path("signup",views.signup, name='signup'),
    path("feedback",views.feedback,name='feedback'),
    path("about",views.about,name="about"),
    path("trans",views.trans,name="trans"),
    #path("logout",views.logout,name="logout"),
    path('logout/', views.logout_view, name='logout'),
    path('emailverify',views.emailverify,name='emailverify'),
    path('verify_otp',views.verify_otp,name="verify_otp"),
    path('verify_otp2',views.verify_otp2,name="verify_otp2"),
    path('send_otp',views.send_otp,name="send_otp"),
    path('send_otp2',views.send_otp2,name="send_otp2"),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('confirm_pass.html',views.confirm_pass,name='confirm_pass'),
   # path('otp2',views.otp2,name="otp2.html"),
    path('process-speech/', views.process_speech, name='process_speech'),
    path('get-supported-languages/', views.get_supported_languages_view, name='get_supported_languages'),
    path('reset',views.reset,name="reset"),
]