from django.db import models

# Create your models here.
class contactus(models.Model):
    cname=models.CharField(max_length=20)
    cemail=models.EmailField()
    csub=models.CharField(max_length=50)
    cmsg=models.CharField(max_length=200)

class appointment(models.Model):
    aname=models.CharField(max_length=20)
    acontact=models.CharField(max_length=10)
    aemail=models.EmailField()
    adate=models.CharField(max_length=10)
    atime=models.CharField(max_length=10)
    amsg=models.CharField(max_length=100)

class lawyer_info(models.Model):
    # OPTION_1 = '1'
    # OPTION_2 = '2'
    # OPTION_3 = '3'
    # OPTION_4 = '4'
    # OPTION_5 = '5'
    # OPTION_6 = '6'
    # EXPERTISE_CHOICE = [
    #     ('OPTION_1','Civil Law'),
    #     ('OPTION_2', 'Family Law'),
    #     ('OPTION_3', 'Business Law'),
    #     ('OPTION_4', 'Education Law'),
    #     ('OPTION_5', 'Criminal Law'),
    #     ('OPTION_6','Cyber Law')
    # ]
    # OPTION_1 = '1'
    # OPTION_2 = '2'
    # OPTION_3 = '3'
    # COURT_CHOICE = [
    #     ('OPTION_1', 'HIGH COURT'),
    #     ('OPTION_2', 'SUPREME COURT'),
    #     ('OPTION_3', 'DISTRICT COURT'),
    # ]
    lemail=models.EmailField()
    lname=models.CharField(max_length=20)
    lprofession=models.CharField(max_length=50)
    limg=models.ImageField(upload_to='image/')
    lexp = models.CharField(max_length=50)
    lexperience=models.CharField(max_length=2)
    lcontact=models.CharField(max_length=10)
    lcourt = models.CharField( max_length=40)
    lstate=models.CharField(max_length=50)
    lpassword=models.CharField(max_length=20)




class client_info(models.Model):
    cname=models.CharField(max_length=20)
    cprofession=models.CharField(max_length=20)
    cdesc=models.CharField(max_length=100)
    cimg = models.ImageField(upload_to='image/')

class case_study(models.Model):
    case=models.CharField(max_length=30)
    title=models.CharField(max_length=50)
    ctime=models.CharField(max_length=20)
    case_img=models.ImageField(upload_to='image/')
    case_type=models.CharField(max_length=100)

class case_desc(models.Model):
    case_title = models.CharField(max_length=100)
    case_intro=models.CharField(max_length=3000)
    case_challenge = models.CharField(max_length=3000)
    case_result = models.CharField(max_length=3000)

class blog(models.Model):
    # OPTION_1 = '1'
    # OPTION_2 = '2'
    # OPTION_3 = '3'
    # OPTION_4 = '4'
    # OPTION_5 = '5'
    # OPTION_6 = '6'
    # BLOG_CHOICE = [
    #     ('OPTION_1', 'Civil Law'),
    #     ('OPTION_2', 'Family Law'),
    #     ('OPTION_3', 'Business Law'),
    #     ('OPTION_4', 'Education Law'),
    #     ('OPTION_5', 'Criminal Law'),
    #     ('OPTION_6', 'Cyber Law')
    # ]
    btitle=models.CharField(max_length=100)
    bimg = models.ImageField(upload_to='image/')
    btype = models.CharField(max_length=50)
    btime=models.CharField(max_length=20)
    bdesc=models.CharField(max_length=5000)

class Newsletter(models.Model):
    email=models.EmailField()

class Court(models.Model):
    court_name=models.CharField(max_length=40)
    desc=models.CharField(max_length=2000)

class law(models.Model):
    name=models.CharField(max_length=50)
    definition=models.CharField(max_length=50)
    law_desc=models.CharField(max_length=2000)