from django.db import models

# Create your models here.
# class sign(models.Model):
#     name=models.CharField(max_length=30)
#     email=models.EmailField()
#     password=models.CharField(max_length=30)

class client_instructions(models.Model):
    cname=models.CharField(max_length=30)
    cdate=models.CharField(max_length=20)
    cinst=models.CharField(max_length=200)
    case = models.CharField(max_length=30)
    clawyer=models.CharField(max_length=30)

class lawyer_timetable(models.Model):
    tname=models.CharField(max_length=30)
    tdate=models.CharField(max_length=20)
    ttime=models.CharField(max_length=20)
    tmsg=models.CharField(max_length=200)

class review(models.Model):
    name=models.CharField(max_length=30)
    email=models.EmailField()
    feedback=models.CharField(max_length=50)