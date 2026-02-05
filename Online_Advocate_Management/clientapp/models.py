from django.db import models

# Create your models here.
class signup(models.Model):
    name=models.CharField(max_length=30)
    email=models.EmailField()
    country=models.CharField(max_length=30)
    password=models.CharField(max_length=30)
    img=models.ImageField(upload_to='image/')
    phone=models.CharField(max_length=10)
    lawyer=models.CharField(max_length=30)

class upload_document(models.Model):
    client_name = models.CharField(max_length=100)
    document_file = models.FileField(upload_to='images/')
    upload_date = models.DateTimeField(auto_now_add=True)
    lawyer_name=models.CharField(max_length=100)

class plan(models.Model):
    name=models.CharField(max_length=20)
    price=models.IntegerField()
    d1=models.CharField(max_length=30)
    d2 = models.CharField(max_length=30)
    d3 = models.CharField(max_length=30)
    d4 = models.CharField(max_length=30)
    d5 = models.CharField(max_length=30)

class Order(models.Model):
    uid = models.ForeignKey(signup, models.CASCADE)
    amt = models.CharField(max_length=10)
    email = models.EmailField()
    firstname = models.CharField(max_length=10)
    # payment_status = models.CharField(max_length=20, default='pending')
