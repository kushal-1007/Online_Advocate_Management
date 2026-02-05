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
from adminapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('/index',views.index ),
    path('/register',views.register),
    path('/show_1',views.show_1),
    path('', views.sign),
    path('/show_appointment', views.show_appointment),
    path('/lawyer_show', views.lawyer_show),
    path('/case_1', views.case_1),
    path('/showclientfeedback', views.showclientfeedback),
    path('/showclient', views.showclient),
    path('/addlawyer', views.addlawyer),
    path('/blog_form', views.blog_form),
    path('/addCase', views.addCase),
    path('/updatelawyer/<int:id>', views.updatelawyer),
    path('/deletelawyer/<int:id>', views.deletelawyer),
    path('/deletecase/<int:id>', views.deletecase),
    path('/blog_show', views.blog_show),
    path('/updateblog/<int:id>', views.updateblog),
    path('/deleteBlog/<int:id>', views.deleteBlog),
    path('/showlawyerfeedback', views.showlawyerfeedback),
    # path('/update_ap/<int:id>', views.update_ap),
    # path('/delete_ap/<int:id>', views.delete_ap),
    path('/updatecase/<int:id>', views.updatecase),
    path('/updateclient/<int:id>', views.updateclient),
    path('/deleteclient/<int:id>', views.deleteclient),
    path('/addCourt',views.addCourt),
    path('/showCourt', views.showCourt),
    path('/updateCourt/<int:id>', views.updateCourt),
    path('/deleteCourt/<int:id>', views.deleteCourt),
    path('/addLaw',views.addLaw),
    path('/show_law', views.show_law),
    path('/updateLaw/<int:id>',views.updateLaw),
    path('/deleteLaw/<int:id>',views.deleteLaw),
    path('/price_plan',views.price_plan),
    path('/showplan',views.showplan),
    path('/update_plan/<int:id>', views.update_plan),
    path('/delete_plan/<int:id>', views.delete_plan),
    path('/showpayment', views.showpayment)

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
