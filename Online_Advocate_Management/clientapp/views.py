from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404

from lawyerapp.models import client_instructions
from myapp.models import client_info, lawyer_info
from .models import signup, upload_document, plan, Order
import razorpay
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def index(request):
    # data=signup.objects.all()
    client_name = request.session.get('cname')
    if client_name:
        client = signup.objects.get(name=client_name)
        client_image = client.img.url  # Assuming img is the image field in your signup model
        return render(request, 'client/index.html', {'client_image': client_image})
    # return render(request, 'client/index.html')


def forgetpassword(request):
    if request.POST:
        e = request.POST['email']
        count = signup.objects.filter(email=e).count()
        data = signup.objects.get(email=e)
        if count > 0:
            subject = 'Thank you for registering to our site'
            name = 'Your name is    ' + data.name + '    ' + 'Your email is ' + e + '     ' + 'Your password is ' + data.password
            # email = 'Your email is '+e
            # password = ' Your password is  '+data.password
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [e, 'kushaltrivedi82@gmail.com']
            send_mail(subject, name, email_from, recipient_list)
            return redirect('/clientapp')
    return render(request, 'client/forget_password.html')


def login_1(request):
    if request.session.get("islogin"):
        return redirect('/clientapp/index')
    if request.POST:
        # u = request.POST['uname']
        e = request.POST['email']
        p = request.POST['password']
        count = signup.objects.filter(email=e, password=p).count()
        if count > 0:
            request.session['islogin'] = True
            # request.session['cname'] = u
            request.session['user_id'] = signup.objects.values('id').filter(email=e, password=p)[0]['id']
            request.session['cname'] = signup.objects.values('name').filter(email=e, password=p)[0]['name']
            return redirect('/clientapp/index')
    return render(request, 'client/login.html')

def logout(request):
    del request.session['islogin']
    return redirect('/clientapp')


def showlawyerinstructions(request):
    client_name = request.session.get('cname')
    client = signup.objects.get(name=client_name)
    client_image = client.img.url  # Assuming img is the image field in your signup model

    # Retrieve the lawyer associated with the client
    client = signup.objects.get(name__iexact=client_name)
    lawyer_name = client.lawyer

    # Filter client instructions based on client name and lawyer name
    data = client_instructions.objects.filter(cname__iexact=client_name, clawyer__iexact=lawyer_name)
    return render(request, 'client/showlawyerinstructions.html', {'data': data, 'client_image': client_image})
    # return render(request, 'client/showlawyerinstructions.html', {'data': data})
    # data = client_instructions.objects.all
    # return render(request, 'client/showlawyerinstructions.html',{'data':data})


def feedback(request):
    client_name = request.session.get('cname')
    client_id = request.session.get('user_id')
    client = signup.objects.get(name=client_name)
    image = client.img.url
    image_1 = image.split("media/")[-1]
    feedback_submitted = client_info.objects.filter(id=client_id).exists()
    print(client_id)
    # print(feedback_submitted)
    if request.POST:
        n = request.POST['name']
        f = request.POST['cdesc']
        profession = request.POST['profession']
        # img = request.FILES['cimg']
        img = image_1
        obj = client_info(cname=n, cprofession=profession, cdesc=f, cimg=img, id=client_id)
        client = request.session.get('id')
        count = client_info.objects.filter(id=client).count()
        if count == 1:
            return redirect("/clientapp/index")
        obj.save()
        return redirect("/clientapp/feedback")
        # obj = client_info(cname=n, cprofession=profession, cdesc=f, cimg=i,id=client_id)

    return render(request, 'client/feedback.html', {'image': image, 'feedback_submitted': feedback_submitted})

    # return render(request, 'client/feedback.html',{'image':image})


def upload_document_view(request):
    client_name = request.session.get('cname')
    data = signup.objects.get(name=client_name)
    client_image = data.img.url
    # cname=request.session.get('cname')
    # data = signup.objects.get(name=cname)

    if request.method == 'POST':
        client_name = request.POST['client_name']
        document_file = request.FILES['document_file']
        lawyer_name = request.POST['lawyer_name']
        obj = upload_document(client_name=client_name, document_file=document_file, lawyer_name=lawyer_name)
        obj.save()
        return redirect('/clientapp/index')
    return render(request, 'client/upload_documents.html', {'client_image': client_image, 'data': data})

def transfer(request):
    client_name = request.session.get('cname')
    name = signup.objects.get(name=client_name)
    data=plan.objects.all()
    lawyername = name.lawyer
    if request.POST:
        request.session['id']=request.POST['plan_id']
        return redirect('/clientapp/payment_process')
    # # if request.POST:
    # #     p=request.POST['price']
    # #     request.session['price']=p
    return render(request,'client/transfer.html',{'data':data,'lawyername':lawyername})


# def payment_process(request):
#     # Razorpay KeyId and key Secret
#     key_id = 'rzp_test_PvM4GxK9MYlCUc'
#     key_secret = 'WzsOTRAU4l3oAA1CS7jlVS5E'
#     plan_id=request.session.get('id')
#     data=plan.objects.get(id=plan_id)
#     plan_name=data.name
#
#     # Retrieve the plan object based on some criteria (e.g., plan name)
#     # Adjust this query according to your requirements
#     selected_plan = get_object_or_404(plan, name=plan_name)
# #
#     # Calculate the amount based on the selected plan's price
#     amount = selected_plan.price * 100  # Convert to cents for Razorpay
#
#     client = razorpay.Client(auth=(key_id, key_secret))
#     data = {
#         'amount': amount,
#         'currency': 'INR',
#         "receipt": "Client Appointment",
#         "notes": {
#             'name': 'Online Advocate Management',
#             'payment_for': 'Client Appointment'
#         }
#     }
#
#     user_id = request.session.get('user_id')
#     result = signup.objects.get(pk=user_id)
#     payment = client.order.create(data=data)
#     context = {'payment': payment, 'result': result}
#     return render(request, 'client/payment_process.html', context)

def complete(request):
    plan_id = request.session.get('id')
    data = plan.objects.get(id=plan_id)
    plan_name = data.name

    # Retrieve the plan object based on some criteria (e.g., plan name)
    # Adjust this query according to your requirements
    selected_plan = get_object_or_404(plan, name=plan_name)

    # Calculate the amount based on the selected plan's price
    amount = selected_plan.price * 100  # Convert to cents for Razorpay
    main_amount = amount / 100
    id = request.session.get('user_id')
    result = signup.objects.get(pk=id)
    user_id = request.session.get('user_id')
    user = signup.objects.get(pk=id)
    e = result.email  # Fetching email from signup object
    fn = result.name
    # order1.uid_id = user.id
    order1 = Order(uid_id=id, amt=main_amount, email=e, firstname=fn)
    order1.save()
    return redirect('/clientapp/success')


def payment_process(request):
    # Razorpay KeyId and key Secret
    key_id = 'rzp_test_PvM4GxK9MYlCUc'
    key_secret = 'WzsOTRAU4l3oAA1CS7jlVS5E'
    client = razorpay.Client(auth=(key_id, key_secret))
    plan_id = request.session.get('id')
    data = plan.objects.get(id=plan_id)
    plan_name = data.name

    # Retrieve the plan object based on some criteria (e.g., plan name)
    # Adjust this query according to your requirements
    selected_plan = get_object_or_404(plan, name=plan_name)

    # Calculate the amount based on the selected plan's price
    amount = selected_plan.price * 100  # Convert to cents for Razorpay
    main_amount=amount/100

    data = {

        'amount': amount,
        'currency': 'INR',
        "receipt": "Client Appointment",
        "notes": {
            'name': 'Online Advocate Management',
            'payment_for': 'Client Appointment'
        }
    }
    id = request.session.get('user_id')
    result = signup.objects.get(pk=id)
    payment = client.order.create(data=data)
    context = {'payment': payment, 'result': result}
    return render(request, 'client/payment_process.html', context)

def success(request):
    context = {}
    return render(request, 'client/success.html', context)

# def payment_process(request):
#     # Razorpay KeyId and key Secret
#     key_id = 'rzp_test_PvM4GxK9MYlCUc'
#     key_secret = 'WzsOTRAU4l3oAA1CS7jlVS5E'
#     client = razorpay.Client(auth=(key_id, key_secret))
#     plan_id = request.session.get('id')
#     data = plan.objects.get(id=plan_id)
#     plan_name = data.name
#
#     # Retrieve the plan object based on some criteria (e.g., plan name)
#     # Adjust this query according to your requirements
#     selected_plan = get_object_or_404(plan, name=plan_name)
#
#     # Calculate the amount based on the selected plan's price
#     amount = selected_plan.price * 100  # Convert to cents for Razorpay
#     main_amount=amount/100
#
#     data = {
#
#         'amount': amount,
#         'currency': 'INR',
#         "receipt": "Client Appointment",
#         "notes": {
#             'name': 'Online Advocate Management',
#             'payment_for': 'Client Appointment'
#         }
#     }
#     id = request.session.get('user_id')
#     result = signup.objects.get(pk=id)
#     payment = client.order.create(data=data)
#     user_id = request.session.get('user_id')
#     user = signup.objects.get(pk=id)
#     e = result.email  # Fetching email from signup object
#     fn = result.name
#     # order1.uid_id = user.id
#     order1 = Order(uid_id=id,amt=main_amount, email=e, firstname=fn)
#     order1.save()
#     context = {'payment': payment, 'result': result}
#     return render(request, 'client/payment_process.html', context)
#
# @csrf_exempt
# def success(request):
#     context = {}
#     return render(request, 'client/success.html', context)


def client_video_call(request):
    client_name = request.session.get('cname')
    return render(request, 'client/client_video_call.html',{'client_name':client_name})
