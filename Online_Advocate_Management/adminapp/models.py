from django.db import models

# Create your models here.
class adminrecord(models.Model):
    aemail=models.EmailField()
    apassword=models.CharField(max_length=20)

    #whatsapp
    #chatbot
