#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User

# ------------------------------------------------------------------------------
#                               Users class.
# ------------------------------------------------------------------------------
class Users(models.Model):
    username = models.OneToOneField(User);
    email = models.CharField(max_length=30);
    # Professor or student
    type_user = models.CharField(max_length=1);
    # Sign up day
    day = models.DateField(auto_now=True);

    # Alphabetical Order  
    class Meta:
        verbose_name_plural = u'Users'
        ordering = ['username']

    def __unicode__(self):
        return self.username;
        
# ------------------------------------------------------------------------------
#                               Universities class.
# ------------------------------------------------------------------------------
class Universities(models.Model):
    noun = models.CharField(max_length=50);  
    country = models.CharField(max_length=50);

    # Alphabetical Order  
    class Meta:
        verbose_name_plural = u'Universities'
        ordering = ['country', 'noun']

    def __unicode__(self):
        return self.country + " - " + self.noun;

# ------------------------------------------------------------------------------
#                               Countries class.
# ------------------------------------------------------------------------------
class Countries(models.Model):
    country = models.CharField(max_length=50);

    # Alphabetical Order  
    class Meta:
        verbose_name_plural = u'Countries'
        ordering = ['country']

    def __unicode__(self):
        return self.country;

# ------------------------------------------------------------------------------
#                               Comment class.
# ------------------------------------------------------------------------------
class Comment(models.Model):
    username = models.CharField(max_length=30);
    title = models.CharField(max_length=30);
    text = models.TextField(help_text="Comenta lo que opinas");
    # Image data is stored in the city folder, title=comment title: 
    image = models.ImageField(upload_to='city', verbose_name=u'title' , blank=True, null=True)
    # Publication day
    day_publicated = models.DateField();
    time = models.DateTimeField(auto_now=True);

    # Alphabetical Order  
    class Meta:
        verbose_name_plural = u'Comment'
        ordering = ['-time']

    def __unicode__(self):
        return str(self.day) + " - " + self.username + ": " + self.title;
        
# ------------------------------------------------------------------------------
#                               University class.
# ------------------------------------------------------------------------------
class University(models.Model):
    uni = models.CharField(max_length=50);  
    # Scholarship: Erasmus or Mundus
    scholarship = models.CharField(max_length=10);

    # Alphabetical Order  
    class Meta:
        #verbose_name_plural = u'University'
        ordering = ['uni']

    def __unicode__(self):
        return self.uni; 

# ------------------------------------------------------------------------------
#                               Info class.
# ------------------------------------------------------------------------------
class InfoBasic(models.Model):
    # Basic
    uni = models.OneToOneField(University);
    address = models.CharField(max_length=50);
    city = models.CharField(max_length=50);
    country = models.CharField(max_length=50);
    latitud = models.DecimalField(default=0, max_digits=10, decimal_places=8);
    longitud = models.DecimalField(default=0, max_digits=10, decimal_places=8);
    description = models.TextField(help_text='Cómo describirías esta universidad');
    link = models.URLField();
    image = models.URLField();
    comment = models.ForeignKey(Comment);

    # Alphabetical Order  
    class Meta:
        verbose_name_plural = u'Basic'
        ordering = ['uni']
        
    def __unicode__(self):
        return self.uni; 


class InfoStadistic(models.Model):
    # Stadistics
    uni = models.OneToOneField(University);
    nuser = models.IntegerField(default=0);
    ncomments = models.IntegerField(default=0);
    score = models.IntegerField(default=0);
    
    # Alphabetical Order  
    class Meta:
        verbose_name_plural = u'Stadistics'
        ordering = ['uni']
        
    def __unicode__(self):
        return self.uni; 

class InfoGeneral(models.Model):
    # Documentation
    uni = models.OneToOneField(University);
    qualification = models.TextField(help_text='Escribe algo', null=True, blank=True);
    specialty = models.TextField(help_text='Escribe algo', null=True, blank=True);
    teachingequipment = models.TextField(help_text='Escribe algo', null=True, blank=True);

    librariy = models.TextField(help_text='Escribe algo', null=True, blank=True);
    lab = models.TextField(help_text='Escribe algo', null=True, blank=True);
    computerequipment = models.TextField(help_text='Escribe algo', null=True, blank=True);

    others = models.TextField(help_text='Escribe algo', null=True, blank=True);
    dinningroom = models.TextField(help_text='Escribe algo', null=True, blank=True);
    cafeteria = models.TextField(help_text='Escribe algo', null=True, blank=True);
    sportactivities = models.TextField(help_text='Escribe algo', null=True, blank=True);
    asociation = models.TextField(help_text='Escribe algo', null=True, blank=True);
    languagecourse = models.TextField(help_text='Escribe algo', null=True, blank=True);
    schoolyear = models.TextField(help_text='Escribe algo', null=True, blank=True);
    vacations = models.TextField(help_text='Escribe algo', null=True, blank=True);
    compteleco = models.TextField(help_text='Escribe algo', null=True, blank=True);

    teachers = models.TextField(help_text='Escribe algo', null=True, blank=True);
    teaching = models.TextField(help_text='Escribe algo', null=True, blank=True);
    studies = models.TextField(help_text='Escribe algo', null=True, blank=True);

    # CostumeService
    costume = models.TextField(help_text='Escribe algo', null=True, blank=True);
    meetings = models.TextField(help_text='Escribe algo', null=True, blank=True);
    offices = models.TextField(help_text='Escribe algo', null=True, blank=True);

    # Documentation
    unidoc = models.TextField(help_text='Escribe algo', null=True, blank=True);
    residencelicence = models.TextField(help_text='Escribe algo', null=True, blank=True);
    getresidence = models.TextField(help_text='Escribe algo', null=True, blank=True);
    economicaid = models.TextField(help_text='Escribe algo', null=True, blank=True);
    bankaccount = models.TextField(help_text='Escribe algo', null=True, blank=True);
     
    #Work
    scholarships = models.TextField(help_text='Escribe algo', null=True, blank=True);
    practices = models.TextField(help_text='Escribe algo', null=True, blank=True);
    contact = models.TextField(help_text='Escribe algo', null=True, blank=True);

    # Comments    
    comment = models.ForeignKey(Comment);

    # Alphabetical Order  
    class Meta:
        verbose_name_plural = u'General'
        ordering = ['uni']
        
    def __unicode__(self):
        return self.uni; 

# ------------------------------------------------------------------------------
#                               Residence class.
# ------------------------------------------------------------------------------
class Residence(models.Model):
    resi = models.CharField(max_length=50);
    uni = models.CharField(max_length=50);
    address = models.CharField(max_length=60);
    latitud = models.DecimalField(default=0, max_digits=6, decimal_places=4);
    longitud = models.DecimalField(default=0, max_digits=6, decimal_places=4);
    comment = models.ForeignKey(Comment);

    # Alphabetical Order  
    class Meta:
        ordering = ['resi']

    def __unicode__(self):
        return self.resi;


class InfoResidence(models.Model):
    uni = models.OneToOneField(University);
    residence = models.ForeignKey(Residence);
    flatshare = models.TextField(help_text='Dónde poder buscar pisos');
    
    # Alphabetical Order  
    class Meta:
        verbose_name_plural = u'Residences'
        ordering = ['uni']
        
    def __unicode__(self):
        return self.uni; 

# ------------------------------------------------------------------------------
#                               Subjects class.
# ------------------------------------------------------------------------------
class Subjects(models.Model):
    subname = models.CharField(max_length=20);
    university = models.ForeignKey(University);
    credits = models.IntegerField(default=0);
    comment = models.ForeignKey(Comment);
    
    # Alphabetical Order  
    class Meta:
        ordering = ['subname']
        
    def __unicode__(self):
        return self.uni;
        


# ------------------------------------------------------------------------------
#                               UserProfile class.
# ------------------------------------------------------------------------------
class UserProfile(models.Model):
    username = models.OneToOneField(User);
    name = models.CharField(max_length=30, null=True, blank=True);
    lastname = models.CharField(max_length=30, null=True, blank=True);
    description = models.TextField(help_text='Escribe tus pensamientos, frases', null=True, blank=True)
    n_university = models.IntegerField(default=0);
    # Image data is stored in the profiles folder, title: Image
    image = models.ImageField(upload_to='profiles', verbose_name=u'username', blank=True, null=True)
    uni1 = models.CharField(max_length=30, null=True, blank=True);
    uni2 = models.CharField(max_length=30, null=True, blank=True);
    university = models.ForeignKey(University);
    # Scholarship Erasmus
    sserasmus = models.CharField(max_length=10, null=True, blank=True);
    # Scholarship Mundus
    ssmundus = models.CharField(max_length=10, null=True, blank=True);

    # Alphabetical Order  
    class Meta:
        ordering = ['username']
    
    def __unicode__(self):
        return self.username;
     
# ------------------------------------------------------------------------------
#                               UserUniversity class.
# ------------------------------------------------------------------------------
class UsersUniversity(models.Model):
    uni = models.CharField(max_length=30);
    nusers = models.IntegerField(default=0);
    useuni = models.ManyToManyField(User);
    
    # Alphabetical Order  
    class Meta:
        ordering = ['uni']

    def __unicode__(self):
        return self.uni;
        

# ------------------------------------------------------------------------------
#                               City class.
# ------------------------------------------------------------------------------
class City(models.Model):
    city = models.CharField(max_length=20);
    description = models.TextField(help_text='Breve descripción de la ciudad');
    image = models.URLField();
    # Using Google Maps
    latitud = models.DecimalField(default=0, max_digits=6, decimal_places=4);
    longitud = models.DecimalField(default=0, max_digits=6, decimal_places=4);
    comment = models.ForeignKey(Comment);

    # Alphabetical Order  
    class Meta:
        ordering = ['city']

    def __unicode__(self):
        return self.city;



