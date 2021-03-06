#encoding:utf-8
##########################################################################
# @Author : Rawan Nazmi-Issa Khozouz                                     #
# @Date : 18/09/13.                                                      #
# @Description : Views that handle the urls selected.                    #
##########################################################################

# Libraries.

# Forms
from django.forms import ModelForm
from django import forms

# Auth
from django.contrib import auth
from django.contrib.auth.models import User

#CSRF
from django.core.context_processors import csrf

# Cross Site Request Forgery protection
from django.views.decorators.csrf import csrf_exempt

# HTTP messages.
from django.http import HttpResponse, Http404, HttpResponseRedirect

# HTML short way for rendering.
from django.shortcuts import render_to_response, get_object_or_404

# HTML rendering libraries.
from django.template import RequestContext, loader

# Sending HTML (Importamos la librería para enviar los correos)
from django.core.mail import EmailMessage, EmailMultiAlternatives 

# Database tables.  
from tuerasmus.models import Users, Universities, UserProfile, Countries

# Forms
from tuerasmus.forms import RegisterForm, ContactForm

# Own libraries.
import parserXML

# Datetime
from datetime import datetime

# Create the XML parser.
parser = parserXML.myContentHandler();

 
# =======================================================================
#                       LOADING DATA METHODS
# =======================================================================

# Name : LOAD UNIVERSITIES to DB
# This method removes all the universities that are in the database and
# reload them from xml files at /data/tuerasmus.

def loadUniversity(request):

    # Remove all the universities.
    Universities.objects.all().delete()

    # Parse the universities
    parser.parseUniversity()

    # Return the template
    return HttpResponseRedirect('/tuerasmus')


# =======================================================================
#                       TuErasmus methods
# =======================================================================

#----------------------------------------------------------------------
#----------------------------------------------------------------------
#Desactivation of CSRF
@csrf_exempt

# Name: INDEX
# The main method 
def index(request):
    if request.user.is_authenticated():
        print "INDEX: usuario logueado " + request.user.username
        ur = '/tuerasmus/' + request.user.username
        print "LOGGEDIN: " + ur
        return HttpResponseRedirect(ur)
    else:
        c = {}
        c.update(csrf(request))
        print "INDEX: usuario no logueado"
        return render_to_response('registration/index.html', c, context_instance=RequestContext(request))

#----------------------------------------------------------------------
#----------------------------------------------------------------------
# Name: AUTH_VIEW
# To check if user is logged or not.
def auth_view(request):
    print "AUTH_VIEW: estoy haciendo login de usuario " + request.user.username
    if request.user.is_authenticated():
        print "ya hay un usuario logueado " + request.user.username
        return HttpResponseRedirect('/tuerasmus')
    else:
        print "Vamos a loguear al usuario"
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            print "Ha sido autenticado, se loguea"
            auth.login(request, user)
            return HttpResponseRedirect('/accounts/loggedin')
        else:
            print "No ha sido autenticado"
            return HttpResponseRedirect('/accounts/invalid')
            
#----------------------------------------------------------------------
#----------------------------------------------------------------------
# Name: LOGGEDIN 
# The user is logged in.
def loggedin(request):
    ur = '/tuerasmus/' + request.user.username
    print "LOGGEDIN: " + ur
    return HttpResponseRedirect(ur)

#----------------------------------------------------------------------
#----------------------------------------------------------------------
# Name: INVALID_LOGIN
# Login was invalid
def invalid_login(request):
    print "INVALID: los datos introducidos son incorrectos"
    ctx = {'alertlogin': True}   
    return render_to_response('registration/index.html', ctx, context_instance=RequestContext(request))

#----------------------------------------------------------------------
#----------------------------------------------------------------------
# Name: LOGOUT
# User is logged out
def logout(request):
    print "LOGOUT: Logout del usuario"
    auth.logout(request)
    return HttpResponseRedirect('/tuerasmus') 

#----------------------------------------------------------------------
#----------------------------------------------------------------------
# Name: REGISTER
# Registering user
def register(request):
    if request.user.is_authenticated():
        print "REGISTER: usuario logueado " + request.user.username
        return HttpResponseRedirect('/tuerasmus')
    else:
        alerterror=""
        alertdone=""
        usu=""
        form = RegisterForm()

        # Method request POST
        if request.method=="POST":
            form = RegisterForm(request.POST)

            # Valid form
            if form.is_valid():
                # Get the information form
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                type_user = request.POST['type_user']
                genero = request.POST['genero']
                password_one = form.cleaned_data['password_one']
                password_two = form.cleaned_data['password_two']
                # Take the time automatically
                day = datetime.now()
                print "day " + str(day)
                       
                # Cheking the information
                if (" " in username) or (username==""):
                    alerterror= True
                elif (" " in password_one) or (password_one=="") or (len(password_one)<6):
                    alerterror= True
                else:
                    # Saving data in DB
                    u = User.objects.create_user(username=username, password=password_one)
                    u.save()

                    us = Users(username=u, email=email, type_user=type_user, genero=genero, day=day)
                    us.save()

                    up = UserProfile(username=u)
                    up.save()

                    form = RegisterForm()
                    alertdone = True
                    usu = username
                
                # Return the template                                 
                ctx = {'form': form, 'alertdone':alertdone, 'alerterror': alerterror, 'usu':usu}
                return render_to_response('registration/register.html', ctx, context_instance=RequestContext(request))
    
            # Form not valid
            else:
                ctx = {'form': form, 'alerterror': True }
                return render_to_response('registration/register.html', ctx, context_instance=RequestContext(request))

        # Method request not POST
        else:
            ctx = {'form': form }
            return render_to_response('registration/register.html', ctx, context_instance=RequestContext(request))

#----------------------------------------------------------------------
#----------------------------------------------------------------------
# Name: HOWTO
# How the website works
def howto(request):
    if request.user.is_authenticated():
        print "HOWTO: usuario logueado " + request.user.username
        return HttpResponseRedirect('/tuerasmus')
    else:
        c = {}
        c.update(csrf(request))
        print "HOWTO: usuario no logueado"
        return render_to_response('registration/howto.html', c, context_instance=RequestContext(request))

#----------------------------------------------------------------------
#----------------------------------------------------------------------
# Name: CONTACT
# How to contact the browser 
def contact(request):
    print "CONTACT: Contactar con el desarrollador"

    type_user=""
    try:
        # Getting if user is student or professor
        t = User.objects.get(username=request.user.username)
        tt = t.username
        tu = Users.objects.all()
        for i in tu:
            if (tt == str(i.username)):
                type_user = str(i.type_user)
        u = request.user.username
    except User.DoesNotExist:
        u=""
    
    # Return the template
    ctx = {'username': u, 'type_user':type_user}
    return render_to_response('registration/contact.html', ctx, context_instance=RequestContext(request))
 
#----------------------------------------------------------------------
#----------------------------------------------------------------------
# Name: CONTACTFORM
# How to contact the browser 
def contactform(request):
    print "CONTACTFORM: Contactar con el desarrollador"

    type_user=""
    try:
        # Getting if user is student or professor
        t = User.objects.get(username=request.user.username)
        tt = t.username
        tu = Users.objects.all()
        for i in tu:
            if (tt == str(i.username)):
                type_user = str(i.type_user)
        u = request.user.username
    except User.DoesNotExist:
        u = ""
    
    
    if request.method=="POST":
        form = ContactForm(request.POST)

        # Valid form
        if form.is_valid():
            # Get the information form
            username = form.cleaned_data['username']
            subject = form.cleaned_data['subject']
            message = request.POST['message']
            #sender = request.POST['sender']
            sender = "rawankho@gmail.com"
            #cc_myself = form.cleaned_data['cc_myself']
            
            # Agregamos una variable 'email' y le pasamos los valores del Asunto, Mensaje y el correo destinatario
            email = EmailMessage('subject', 'message', to=['sender']) 
            #Por último enviamos el correo
            email.send() 
            
            ctx = {'alertdone':True, 'username': u, 'type_user':type_user}  
            
            
        # Form not valid
        else:
            ctx = {'form': form, 'alerterror': True, 'username': u, 'type_user':type_user}
            
        return render_to_response('registration/contactform.html', ctx, context_instance=RequestContext(request))

        
    else:
        form = ContactForm()
        # Return the template
        ctx = {'form':form, 'username': u, 'type_user':type_user}
        return render_to_response('registration/contactform.html', ctx, context_instance=RequestContext(request))
   
