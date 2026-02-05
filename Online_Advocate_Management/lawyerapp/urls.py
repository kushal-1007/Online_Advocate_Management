"""
URL configuration for webapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from lawyerapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('/index',views.index),
    path('',views.signin),
    path('/lawyer_video_call',views.lawyer_video_call),
    path('/addTimetable', views.addTimetable),
    path('/updateTimetable/<int:id>', views.updateTimetable),
    path('/deleteTimetable/<int:id>', views.deleteTimetable),
    path('/lawyer_calender_show',views.lawyer_calender_show),
    path('/deleteap/<int:id>', views.deleteap),
    path('/logout',views.logout),
    path('/addInstruction', views.addInstruction),
    path('/showInstruction', views.showInstruction),
    path('/updateinstruction/<int:id>', views.updateinstruction),
    path('/deleteinstruction/<int:id>', views.deleteinstruction),
    path('/feedback_lawyer',views.feedback_lawyer),
    path('/show_documents',views.show_documents),
    path('/forget_password',views.forget_password)
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
