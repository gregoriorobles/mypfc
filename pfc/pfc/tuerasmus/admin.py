##########################################################################
# @Author : Rawan Nazmi-Issa Khozouz                                     #
# @Date : 18/09/13.                                                      #
# @Description : Admin                                                   #
##########################################################################

# Import objects
from django.contrib import admin
from tuerasmus.models import City, Comment, Countries, InfoBasic, InfoGeneral, InfoResidence, InfoStadistics, Residence, Subjects, Universities, University, UserProfile, Users, UsersUniversity

#--------------------------------------
#--------------------------------------
#      Objects editable by admin      #
#--------------------------------------
#--------------------------------------

# Cities
admin.site.register(City)

# Comment
admin.site.register(Comment)

# Countries
admin.site.register(Countries)

# Info
admin.site.register(InfoBasic)
admin.site.register(InfoGeneral)
admin.site.register(InfoResidence)
admin.site.register(InfoStadistics)
admin.site.register(Residence)
admin.site.register(Subjects)

# Universities
admin.site.register(Universities)
admin.site.register(University)

# Signed up users
admin.site.register(Users)

# User's profile
admin.site.register(UserProfile)

# Users that belong to the university
admin.site.register(UsersUniversity)
