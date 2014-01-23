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
from django.core.mail import EmailMessage, EmailMultiAlternatives # Sending HTML

# Database tables.  
from tuerasmus.models import Users, UniErasmus, University, Universities, UserProfile, UsersUniversity, Countries
from tuerasmus.forms import RegisterForm, ProfileForm, UniversityForm

# Own libraries.
import parserXML

# Create the XML parser.
parser = parserXML.myContentHandler();


#Desactivation of CSRF
@csrf_exempt
 
# =======================================================================
#                       LOADING DATA METHODS
# =======================================================================

# Name : LOAD UNIVERSITIES to DB
# This method removes all the universities that are in the database and
# reload them from xml files at /data/tuerasmus.

def loadUniversity(request):

    #Remove all the universities.
    Universities.objects.all().delete()

    #Parse the universities
    parser.parseUniversity()

    #Return the template
    #return index(request)
    return HttpResponseRedirect('/tuerasmus')


# =======================================================================
#                       TuErasmus methods
# =======================================================================

#----------------------------------------------------------------------
#----------------------------------------------------------------------
# Name: INDEX
# The main method 
def index(request):
    if request.user.is_authenticated():
        print "INDEX: usuario logueado " + request.user.username
        ur = '/tuerasmus/home/' + request.user.username
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
    ur = '/tuerasmus/home/' + request.user.username
    print "LOGGEDIN: " + ur
    return HttpResponseRedirect(ur)


#----------------------------------------------------------------------
#----------------------------------------------------------------------
# Name: INVALID_LOGIN
def invalid_login(request):
    print "INVALID: los datos introducidos son incorrectos"
    alertlogin = True
    ctx = {'alertlogin': alertlogin}
    return render_to_response('registration/index.html', ctx, context_instance=RequestContext(request))


#----------------------------------------------------------------------
#----------------------------------------------------------------------
# Name: LOGOUT
def logout(request):
    print "LOGOUT: Logout del usuario"
    auth.logout(request)
    return HttpResponseRedirect('/tuerasmus') 


#----------------------------------------------------------------------
#----------------------------------------------------------------------
# Name: REGISTER
def register(request):
    print "Estoy en register!!!!!!!!!!!!"
    # User registered
    if request.user.is_authenticated():
        print "REGISTER: ya hay un usuario logueado " + request.user.username
        return HttpResponseRedirect('/tuerasmus')

    # User not registered
    else:
        alerterror=""
        alertdone=""
        form = RegisterForm()
        if request.method=="POST":
            # Form with our information
            form = RegisterForm(request.POST)
            
            if form.is_valid():
                username = form.cleaned_data['username']
                if (" " in username) or (username==""):
                    error_msg = "Nombre de usuario no puede tener espacios"
                    return render_to_response('registration/register.html', {'msg':True, 'error_msg':error_msg, 'form':form}, context_instance=RequestContext(request))

#               name = form.cleaned_data['name']
#               lastname = form.cleaned_data['lastname']
#               if (name=="") or (lastname==""):
#                   return HttpResponseRedirect('/accounts/invalid')

                email = form.cleaned_data['email']

#               description = form.cleaned_data['description']
#               university = form.cleaned_data['university']
#               photo = form.cleaned_data['photo']

                type_user = request.POST['type_user']
      
                password_one = form.cleaned_data['password_one']
                if (" " in password_one) or (password_one==""):
                    return HttpResponseRedirect('/accounts/register')

                password_two = form.cleaned_data['password_two']
                day = form.cleaned_data['day']

                u = User.objects.create_user(username=username, password=password_one)
                u.save()

                us = Users(username=u, email=email, type_user=type_user, day=day)
                us.save()

                up = UserProfile(username=u)
                up.save()

#               up = UserProfile(username=u, name=name, lastname=lastname, image=photo, university=university)
#               up.save()

                form = RegisterForm()
                ctx = {'form': form, 'alertdone':True, 'usu': username}
                return render_to_response('registration/register.html', ctx, context_instance = RequestContext(request))
            else:
                alerterror = True
                ctx = {'form': form, 'alerterror': alerterror }
                return render_to_response('registration/register.html', ctx, context_instance=RequestContext(request))
  
#    else: method GET
#        form = RegisterForm()
#        ctx = {'form': form, 'username':username, 'email':email, 'password_one':password_one, 'password_two':password_two}  
  
#        if request.method=="GET":
#            print "ahora tengo un GET, y le paso la info vacia!!!!!!!!!!!!!!!!!!!"
#            form = RegisterForm()
#            ctx = {'form': form, 'username':'', 'email':'', 'password':''}
#            return render_to_response('registration/register.html', ctx, context_instance=RequestContext(request))

        ctx = {'form': form }
        return render_to_response('registration/register.html', ctx, context_instance=RequestContext(request))


#----------------------------------------------------------------------
#----------------------------------------------------------------------
# Name: CONTACT 
def contact(request):
    print "CONTACT: Contactar con el desarrollador"
    type_user=""
    try:
        t = User.objects.get(username=request.user.username)
        tt = t.username
        tu = Users.objects.all()
        for i in tu:
            if (tt == str(i.username)):
                type_user = str(i.type_user)
        u = request.user.username
    except User.DoesNotExist:
        u=""
    
    ctx = {'username': u, 'type_user':type_user}
    return render_to_response('registration/contact.html', ctx, context_instance=RequestContext(request))

   
