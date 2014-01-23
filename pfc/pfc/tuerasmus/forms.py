#encoding:utf-8

##########################################################################
# @Author : Rawan Nazmi-Issa Khozouz                                     #
# @Date : 07/10/13.                                                      #
# @Description : Forms to be used.                                       #
##########################################################################

from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from tuerasmus.models import Users, UniErasmus, University, Universities, UserProfile, UsersUniversity, Countries

import datetime

#----------------------------------------------------------------------------
#            Class RegisterForm: to register the user  
#----------------------------------------------------------------------------     
class RegisterForm(forms.Form):
    username = forms.CharField(label="Nombre de usuario", widget=forms.TextInput(), error_messages={'required': 'Debes introducir un nombre de usuario'})
    email = forms.EmailField(label="Correo electrónico (gmail)", widget=forms.TextInput(), error_messages={'required': 'Debes introducir un correo electrónico', 'invalid':u'Introduce un correo válido'})
    password_one = forms.CharField(label="Contraseña", widget=forms.PasswordInput(render_value=False), error_messages={'required': 'Debes introducir una contraseña'})
    password_two = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput(render_value=False), error_messages={'required': 'Debes volver a introducir la contraseña'})
    day = forms.DateField(label="Fecha de registro", widget=forms.TextInput(), initial=datetime.date.today)

    # Data validation
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            u = User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('Nombre de usuario registrado')

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            e = Users.objects.get(email=email)
        except Users.DoesNotExist:
            return email
        raise forms.ValidationError('Correo electrónico registrado')

    def clean_password_two(self):  
        password_one = self.cleaned_data.get('password_one', '')
        password_two = self.cleaned_data.get('password_two', '')
        if (not password_one):
            error_msg = u'Debes introducir una contraseña'
            self._errors['password_one'] = self.error_class([error_msg]) 
        elif (not password_two):
            error_msg = u'Debes introducir una contraseña'
            self._errors['password_two'] = self.error_class([error_msg])
        elif password_one and password_two and (password_one == password_two):
            pass
        else:
            raise forms.ValidationError('Contraseñas no coinciden')


#----------------------------------------------------------------------------
#            Class ProfileForm: to change the user profile 
#----------------------------------------------------------------------------
class ProfileForm(forms.Form):
    name = forms.CharField(label="Nombre", widget=forms.TextInput(), error_messages={'required': 'Debes introducir tu nombre'})
    lastname = forms.CharField(label="Apellidos", widget=forms.TextInput(), error_messages={'required': 'Debes introducir tus apellidos'})
    description = forms.CharField(label="Biografía")
    university = forms.CharField(label="Universidad", widget=forms.TextInput())
    uni_reg = forms.BooleanField(required=False)
    photo = forms.ImageField(label="Imagen de perfil", required=False)


#----------------------------------------------------------------------------
#            Class UniversityForm: to register the university  
#----------------------------------------------------------------------------
class UniversityForm(forms.Form):
    acronym = forms.CharField(label="Siglas de la universidad", widget=forms.TextInput(), error_messages={'required': 'Introduce las siglas de la universidad'})
    city = forms.CharField(label="Ciudad de la universidad", widget=forms.TextInput(), error_messages={'required': 'Debes introducir la ciudad'})
    country = forms.CharField(label="País de la universidad", widget=forms.TextInput(), error_messages={'required': 'Debes introducir país'})
    description = forms.CharField(label="Descripción breve sobre la universidad", error_messages={'required': 'Escribe una breve introducción acerca de la universidad'})
    #Revisar como se ponen los link en un formulario!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    location = forms.URLField(label='Coordenadas de su localización', required=False);
    link = forms.URLField(label='Web oficial de la universidad', required=False);
    image = forms.URLField(label='Alguna imagen de la universidad', required=False);


#----------------------------------------------------------------------------
#            Class UniProfileForm: to change the university profile   
#----------------------------------------------------------------------------

class UniProfileForm(forms.Form):
    uni = forms.CharField(label="Nombre de la universidad", widget=forms.TextInput(), error_messages={'required': 'Debes introducir el nombre de la universidad'})
    scholarship = forms.CharField(label="Erasmus/ErasmusMundus", widget=forms.TextInput(), error_messages={'required': 'Debes especificar el tipo de beca'})
    acronym = forms.CharField(label="Siglas de la universidad", widget=forms.TextInput())
    city = forms.CharField(label="Ciudad de la universidad", widget=forms.TextInput(), error_messages={'required': 'Debes introducir la ciudad'})
    country = forms.CharField(label="País de la universidad", widget=forms.TextInput(), error_messages={'required': 'Debes introducir país'})
    description = forms.CharField(label="Descripción breve sobre la universidad")
    ################# REVISAR COMO HACER LOS TIPO URL##############
    location = forms.URLField(label='Coordenadas de su locaclización', required=False);
    link = forms.URLField(label='Web oficial de la universidad', required=False);
    image = forms.URLField(label='Alguna imagen de la universidad', required=False);

    # Data validation
    def clean_uni(self):
        uni = self.cleaned_data['uni']
        try:
            u = University.objects.get(uni=uni)
        except University.DoesNotExist:
            return uni
        raise forms.ValidationError('Universidad registrada')

    def clean_acronym(self):
        acronym = self.cleaned_data['acronym']
        try:
            a = University.objects.get(acronym=acronym)
        except University.DoesNotExist:
            return acronym
        raise forms.ValidationError('Siglas registrada')


