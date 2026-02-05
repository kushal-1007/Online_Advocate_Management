from django.contrib import admin

from adminapp.models import adminrecord
from clientapp.models import signup, upload_document, plan,Order
from .models import *
from lawyerapp.models import review


# Register your models here.

admin.site.register(contactus)
admin.site.register(appointment)
admin.site.register(lawyer_info)
admin.site.register(client_info)
admin.site.register(case_study)
admin.site.register(case_desc)
admin.site.register(blog)
admin.site.register(adminrecord)
admin.site.register(signup)
admin.site.register(review)
admin.site.register(Court)
admin.site.register(law)
admin.site.register(plan)
admin.site.register(Order)
# admin.site.register(sign)