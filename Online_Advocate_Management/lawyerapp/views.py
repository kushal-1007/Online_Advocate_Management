from os.path import basename

import pytz
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404

from clientapp.models import upload_document,signup
from lawyerapp.models import  client_instructions, lawyer_timetable,review
from myapp.models import lawyer_info, appointment


# Create your views here.
def index(request):
    lawyer_name=request.session.get('name')
    client_count = signup.objects.filter(lawyer=lawyer_name).count()
    data=lawyer_info.objects.get(lname=lawyer_name)
    image=data.limg.url
    return render(request,'lawyer/index.html',{'image':image,'client_count':client_count})

def forget_password(request):
    if request.POST:
        e=request.POST['lemail']
        count=lawyer_info.objects.filter(lemail=e).count()
        data=lawyer_info.objects.get(lemail=e)
        if count>0:
            subject = 'Thank you for registering to our site'
            name = 'Your name is    ' + data.lname+'    ' + 'Your email is '+ data.lemail +'     ' + 'Your password is '+data.lpassword
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [e, 'kushaltrivedi82@gmail.com']
            send_mail(subject,name, email_from, recipient_list)
            return redirect('/lawyerapp')
    return render(request,'lawyer/forget_password.html')

def signin(request):
    if request.session.get('is_login'):
        return redirect('lawyerapp/index')
    if request.POST:
        email=request.POST['lemail']
        password=request.POST['password']
        # name=request.POST['lname']
        # count=lawyer_info.objects.filter(lname=name,lemail=email,lpassword=password).count()
        count = lawyer_info.objects.filter(lemail=email, lpassword=password).count()
        if count>0:
            request.session['is_login']=True
            request.session['lawyer_id'] = lawyer_info.objects.values('id').filter(lemail=email, lpassword=password)[0][
                'id']
            request.session['name'] = lawyer_info.objects.values('lname').filter(lemail=email, lpassword=password)[0]['lname']
            return redirect('/lawyerapp/index')
    return render(request,'lawyer/signin.html')

def addInstruction(request):
    lawyer_name = request.session.get('name')
    data = lawyer_info.objects.get(lname=lawyer_name)
    image = data.limg.url
    # Replace '' with a default value if needed
    # Get clients associated with the lawyer
    clients = signup.objects.filter(lawyer__iexact=lawyer_name)
    if request.POST:
        name=request.POST['cname']
        date=request.POST['cdate']
        desc=request.POST['cinst']
        lawyer=request.POST['clawyer']
        case=request.POST['case']
        obj=client_instructions(cname=name,cdate=date,cinst=desc,clawyer=lawyer,case=case)
        obj.save()
        return redirect('/lawyerapp/index')
    return render(request, 'lawyer/addInstruction.html', {'clients': clients,'image':image})

def updateinstruction(request,id):
        lawyer_name = request.session.get('name')
        data = lawyer_info.objects.get(lname=lawyer_name)
        image = data.limg.url

        # Fetch the client instruction object to be updated
        data = client_instructions.objects.get(id=id)

        # Get clients associated with the lawyer
        clients_with_lawyer = signup.objects.filter(lawyer__iexact=lawyer_name)

        # Fetch the client associated with the instruction
        instruction_client = data.cname

        # Exclude the instruction client from the clients associated with the lawyer
        remaining_clients = clients_with_lawyer.exclude(name=instruction_client).values_list('name', flat=True)

        # Construct the clients list with the instruction client at the beginning
        clients = [instruction_client] + list(remaining_clients)
        print(clients)

        if request.method == 'POST':
            # Extract form data
            name = request.POST['cname']
            date = request.POST['cdate']
            desc = request.POST['cinst']
            lawyer = request.POST['clawyer']
            case = request.POST['case']

            # Update client instruction object
            data.cname = name
            data.cdate = date
            data.cinst = desc
            data.clawyer = lawyer
            data.case = case
            data.save()

            return redirect('/lawyerapp/index')

        return render(request, 'lawyer/updateinstruction.html', {'data': data, 'clients': clients,'image':image})


def deleteinstruction(request,id):
    client_instructions.objects.get(id=id).delete()
    return redirect('/lawyerapp/index')

def showInstruction(request):
    lawyer_name = request.session.get('name')
    data = lawyer_info.objects.get(lname=lawyer_name)
    image = data.limg.url
    data=client_instructions.objects.all
    return render(request,'lawyer/showInstruction.html',{'data':data,'image':image})

def logout(request):
    del request.session['is_login']
    return redirect('/lawyerapp')

def deleteap(request,id):
    appointment.objects.get(id=id).delete()
    return redirect('/lawyerapp')

def addTimetable(request):
    lawyer_name = request.session.get('name')
    data = lawyer_info.objects.get(lname=lawyer_name)
    image = data.limg.url
    if request.POST:
        client=request.POST['tname']
        date=request.POST['tdate']
        time=request.POST['ttime']
        msg=request.POST['tmsg']
        obj=lawyer_timetable(tname=client,tdate=date,ttime=time,tmsg=msg)
        obj.save()
        return redirect('/lawyerapp/index')
    return render(request,'lawyer/addtimetable.html',{'image':image})

def updateTimetable(request,id):
    lawyer_name = request.session.get('name')
    data = lawyer_info.objects.get(lname=lawyer_name)
    image = data.limg.url
    data=lawyer_timetable.objects.get(id=id)
    if request.POST:
        client=request.POST['tname']
        date=request.POST['tdate']
        time=request.POST['ttime']
        msg=request.POST['tmsg']
        obj=lawyer_timetable(id=id,tname=client,tdate=date,ttime=time,tmsg=msg)
        obj.save()
        return redirect('/lawyerapp/index')
    return render(request,'lawyer/updateTimetable.html',{'data':data,'image':image})

def lawyer_calender_show(request):
    lawyer_name = request.session.get('name')
    data = lawyer_info.objects.get(lname=lawyer_name)
    image = data.limg.url
    data=lawyer_timetable.objects.all
    return render(request,'lawyer/lawyer_calender.html',{'data':data,'image':image})

def deleteTimetable(request,id):
    lawyer_timetable.objects.get(id=id).delete()
    return redirect('/lawyerapp/index')

def feedback_lawyer(request):
    lawyer_name = request.session.get('name')
    lawyer_id = request.session.get('lawyer_id')
    data = lawyer_info.objects.get(lname=lawyer_name)
    image = data.limg.url
    email=data.lemail
    feedback_submitted = review.objects.filter(id=lawyer_id).exists()
    if request.POST:
        name=request.POST['name']
        email=request.POST['email']
        desc=request.POST['feedback']
        obj=review(id=lawyer_id,name=name,email=email,feedback=desc)
        feed = request.session.get('id')
        count = review.objects.filter(id=feed).count()
        if count == 1:
            return redirect('/lawyerapp/index')
        obj.save()
        return redirect('/lawyerapp/feedback_lawyer')
        # return redirect('/lawyerapp/index')
    return render(request,'lawyer/feedback_lawyer.html',{'email':email,'image':image,'feedback_submitted': feedback_submitted})

def show_documents(request):
    lawyer_name = request.session.get('name')
    data = lawyer_info.objects.get(lname=lawyer_name)
    image = data.limg.url  # Replace with the actual key storing lawyer's name in session

    # Filter documents based on the lawyer's name
    documents = upload_document.objects.filter(lawyer_name__iexact=lawyer_name)

    # Extract client names from documents
    clients_with_documents = documents.values_list('client_name', flat=True).distinct()

    # Get all clients associated with the lawyer
    all_clients = signup.objects.filter(lawyer__iexact=lawyer_name).values_list('name', flat=True).distinct()

    # Combine the lists of clients with and without documents
    all_clients_set = set(all_clients)
    clients_without_documents = list(all_clients_set - set(clients_with_documents))

    # Merge both lists, ensuring clients with documents appear first
    all_clients_merged = list(clients_with_documents) + clients_without_documents

    # Get the selected client name from the request
    selected_client = request.GET.get('client')

    # If a client is selected, filter documents by that client
    if selected_client:
        documents = documents.filter(client_name=selected_client)

    # Extract file names and upload dates
    file_names = [basename(file.document_file.name) for file in documents]
    indian_tz = pytz.timezone('Asia/Kolkata')
    upload_dates = [file.upload_date.astimezone(indian_tz) for file in documents]

    # Format upload dates
    formatted_dates = [date.strftime('%d/%m/%y') for date in upload_dates]
    formatted_times = [date.strftime('%H:%M:%S') for date in upload_dates]

    # Zip files, file_names, and dates together
    files_with_names_and_dates = zip(documents, file_names, formatted_times, formatted_dates)

    return render(request, 'lawyer/show_documents.html',
                  {'files_with_names_and_dates': files_with_names_and_dates, 'clients': all_clients_merged,
                   'selected_client': selected_client,'image':image})
    # lawyer_name = request.session.get('name', '')  # Replace with the actual key storing lawyer's name in session
    #
    # # Filter documents based on the lawyer's name
    # documents = upload_document.objects.filter(lawyer_name__iexact=lawyer_name)
    #
    # # Extract client names
    # clients = documents.values_list('client_name', flat=True).distinct()
    #
    # # Get the selected client name from the request
    # selected_client = request.GET.get('client')
    #
    # # If a client is selected, filter documents by that client
    # if selected_client:
    #     documents = documents.filter(client_name=selected_client)
    #
    # # Extract file names and upload dates
    # file_names = [basename(file.document_file.name) for file in documents]
    # indian_tz = pytz.timezone('Asia/Kolkata')
    # upload_dates = [file.upload_date.astimezone(indian_tz) for file in documents]
    #
    # # Format upload dates
    # formatted_dates = [date.strftime('%d/%m/%y') for date in upload_dates]
    # formatted_times = [date.strftime('%H:%M:%S') for date in upload_dates]
    #
    # # Zip files, file_names, and dates together
    # files_with_names_and_dates = zip(documents, file_names, formatted_times, formatted_dates)
    #
    # return render(request, 'lawyer/show_documents.html',
    #               {'files_with_names_and_dates': files_with_names_and_dates, 'clients': clients,
    #                'selected_client': selected_client})


# def profile(request,name):
#     data=lawyer_info.objects.filter(lname__icontains=name)
#     return render(request,'lawyer/profile.html',{'data':data})

def lawyer_video_call(request):
    lawyer_name=request.session.get('name')
    return render(request, 'lawyer/lawyer_video_call.html',{'lawyer_name':lawyer_name})


