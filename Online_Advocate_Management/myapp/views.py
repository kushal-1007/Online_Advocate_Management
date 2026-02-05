from django.shortcuts import render,redirect,get_object_or_404
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

from .models import contactus, appointment, lawyer_info, client_info, case_study, case_desc, blog, Newsletter, Court,law
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4,letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from bs4 import BeautifulSoup
from django.core.mail import send_mail
import smtplib
from django.conf import settings
import razorpay




# Create your views here.
def index(request):
    data = lawyer_info.objects.all()  # Retrieve all lawyer_info objects
    data1 = client_info.objects.all()  # Retrieve all client_info objects
    data2 = blog.objects.order_by('-btime')  # Retrieve all blog objects ordered by btime
    # data3 = Court.objects.all()  # Retrieve all Court objects

    unique_expertise = set()
    unique_courts = set()

    # Iterate over lawyer_info objects to extract unique court names
    for lawyer in data:
        # Split the lcourt string by commas and add each value to the unique_courts set
        courts = lawyer.lcourt.split(',')
        unique_courts.update(courts)

    # Filter law objects based on unique court names
    data3 = Court.objects.filter(court_name__in=unique_courts)

    # Loop through all lawyer_info objects and collect unique expertise values
    for lawyer in data:
        # Split the lexp string by commas and add each value to the unique_expertise set
        expertise = lawyer.lexp.split(',')
        unique_expertise.update(expertise)

    # Filter law objects based on unique expertise values
    data4 = law.objects.filter(name__in=unique_expertise)

    return render(request, 'myapp/index.html',
                  {'data': data, 'data1': data1, 'data2': data2, 'data3': data3, 'data4': data4})

def court_types(request,name):
    data=lawyer_info.objects.filter(lcourt__icontains=name)
    data1=Court.objects.filter(court_name__icontains=name)
    data5=lawyer_info.objects.all()
    # data3 = Court.objects.all()
    unique_expertise = set()
    unique_courts = set()
    for lawyer in data5:
        # Split the lcourt string by commas and add each value to the unique_courts set
        courts = lawyer.lcourt.split(',')
        unique_courts.update(courts)

        # Filter law objects based on unique court names
    data3 = Court.objects.filter(court_name__in=unique_courts)

    # Loop through all lawyer_info objects and collect unique expertise values
    for lawyer in data5:
        # Split the lexp string by commas and add each value to the unique_expertise set
        expertise = lawyer.lexp.split(',')
        unique_expertise.update(expertise)

    # Filter law objects based on unique expertise values
    data4 = law.objects.filter(name__in=unique_expertise)

    return render(request,'myapp/court_types.html',{'data':data,'name':name,'data1':data1,'data3':data3,'data4':data4})


def News(request):
    if request.POST:
        e=request.POST['email']
        obj=Newsletter(email=e)
        obj.save()
        subject = 'Thank you for registering to our site'
        message = ' it  means a world to us '
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [e,'kushaltrivedi82@gmail.com']
        send_mail(subject, message, email_from, recipient_list)
        return redirect('/#')

def about(request):
    data=lawyer_info.objects.all()
    # data3 = Court.objects.all()
    unique_courts = set()
    unique_expertise=set()
    for lawyer in data:
        # Split the lexp string by commas and add each value to the unique_expertise set
        expertise = lawyer.lexp.split(',')
        unique_expertise.update(expertise)
    # Filter law objects based on unique expertise values
    data4 = law.objects.filter(name__in=unique_expertise)
    for lawyer in data:
        # Split the lcourt string by commas and add each value to the unique_courts set
        courts = lawyer.lcourt.split(',')
        unique_courts.update(courts)


        # Filter law objects based on unique court names
    data3 = Court.objects.filter(court_name__in=unique_courts)
    return render(request,'myapp/about.html',{'data':data,'data3':data3,'data4':data4})

def blog_1(request):
    # data=blog.objects.all
    data = blog.objects.order_by('-btime')
    unique_courts = set()
    data2=lawyer_info.objects.all()
    unique_expertise = set()
    for lawyer in data2:
        # Split the lexp string by commas and add each value to the unique_expertise set
        expertise = lawyer.lexp.split(',')
        unique_expertise.update(expertise)
    # Filter law objects based on unique expertise values
    data4 = law.objects.filter(name__in=unique_expertise)
    for lawyer in data2:
        # Split the lcourt string by commas and add each value to the unique_courts set
        courts = lawyer.lcourt.split(',')
        unique_courts.update(courts)

        # Filter law objects based on unique court names
    data3 = Court.objects.filter(court_name__in=unique_courts)
    return render(request,'myapp/blog.html',{'data':data,'data3':data3,'data4':data4})

def contact(request):
    # data3 = Court.objects.all()
    data5=lawyer_info.objects.all()
    unique_courts = set()
    unique_expertise = set()
    for lawyer in data5:
        # Split the lexp string by commas and add each value to the unique_expertise set
        expertise = lawyer.lexp.split(',')
        unique_expertise.update(expertise)
    # Filter law objects based on unique expertise values
    data4 = law.objects.filter(name__in=unique_expertise)
    for lawyer in data5:
        # Split the lcourt string by commas and add each value to the unique_courts set
        courts = lawyer.lcourt.split(',')
        unique_courts.update(courts)

        # Filter law objects based on unique court names
    data3 = Court.objects.filter(court_name__in=unique_courts)
    if request.POST:
        name=request.POST['name']
        email = request.POST['email']
        sub = request.POST['sub']
        msg = request.POST['msg']
        obj=contactus(cname=name,cemail=email,csub=sub,cmsg=msg)
        obj.save()
        return redirect('/contact')
    return render(request,'myapp/contact.html',{'data3':data3,'data4':data4})

def portfolio(request):
    data=case_study.objects.all
    # data3 = Court.objects.all()
    data5 = lawyer_info.objects.all()
    unique_courts = set()
    unique_expertise = set()
    for lawyer in data5:
        # Split the lexp string by commas and add each value to the unique_expertise set
        expertise = lawyer.lexp.split(',')
        unique_expertise.update(expertise)
    # Filter law objects based on unique expertise values
    data4 = law.objects.filter(name__in=unique_expertise)
    for lawyer in data5:
        # Split the lcourt string by commas and add each value to the unique_courts set
        courts = lawyer.lcourt.split(',')
        unique_courts.update(courts)
        # Filter law objects based on unique court names
    data3 = Court.objects.filter(court_name__in=unique_courts)
    law_categories = set([category.split()[0] for category in case_study.objects.values_list('case', flat=True)])
    return render(request,'myapp/portfolio.html',{'data':data,'data3':data3,'law_categories':law_categories,'data4':data4})

def service(request):
    data=lawyer_info.objects.all()
    # data3 = Court.objects.all()
    unique_expertise = set()
    unique_courts = set()
    for lawyer in data:
        # Split the lcourt string by commas and add each value to the unique_courts set
        courts = lawyer.lcourt.split(',')
        unique_courts.update(courts)

        # Filter law objects based on unique court names
    data3 = Court.objects.filter(court_name__in=unique_courts)

    # Loop through all lawyer_info objects and collect unique expertise values
    for lawyer in data:
        # Split the lexp string by commas and add each value to the unique_expertise set
        expertise = lawyer.lexp.split(',')
        unique_expertise.update(expertise)

    # Filter law objects based on unique expertise values
    data4 = law.objects.filter(name__in=unique_expertise)
    return render(request,'myapp/service.html',{'data':data,'data3':data3,'data4':data4})

# def single(request):
#     return render(request,'myapp/single.html')

def team(request):
    data = lawyer_info.objects.all()
    # data3 = Court.objects.all()
    unique_expertise = set()
    for lawyer in data:
        # Split the lexp string by commas and add each value to the unique_expertise set
        expertise = lawyer.lexp.split(',')
        unique_expertise.update(expertise)
    # Filter law objects based on unique expertise values
    data4 = law.objects.filter(name__in=unique_expertise)
    unique_courts = set()
    for lawyer in data:
        # Split the lcourt string by commas and add each value to the unique_courts set
        courts = lawyer.lcourt.split(',')
        unique_courts.update(courts)

        # Filter law objects based on unique court names
    data3 = Court.objects.filter(court_name__in=unique_courts)
    return render(request,'myapp/team.html',{'data':data,'data3':data3,'data4':data4})

def show(request):
    data=contactus.objects.all
    return render(request,'myapp/show.html',{'data':data})

def update(request,id):
    data=contactus.objects.get(id=id)
    if request.POST:
        name=request.POST['name']
        email = request.POST['email']
        sub = request.POST['sub']
        msg = request.POST['msg']
        obj=contactus(cname=name,cemail=email,csub=sub,cmsg=msg,id=id)
        obj.save()
        return redirect('/show')
    return render(request,'myapp/update.html',{'data':data})

def delete(request,id):
    contactus.objects.get(id=id).delete()
    return redirect('/show')

def lawtype(request,name):
    data = lawyer_info.objects.filter(lexp__icontains=name)
    data1=client_info.objects.all()
    data2=law.objects.filter(name__icontains=name)
    data5=lawyer_info.objects.all()
    unique_courts = set()
    unique_expertise = set()
    for lawyer in data5:
        # Split the lexp string by commas and add each value to the unique_expertise set
        expertise = lawyer.lexp.split(',')
        unique_expertise.update(expertise)
    # Filter law objects based on unique expertise values
    data4 = law.objects.filter(name__in=unique_expertise)
    for lawyer in data5:
        # Split the lcourt string by commas and add each value to the unique_courts set
        courts = lawyer.lcourt.split(',')
        unique_courts.update(courts)

        # Filter law objects based on unique court names
    data3 = Court.objects.filter(court_name__in=unique_courts)
    return render(request,'myapp/law_type.html',{'data':data,'data1':data1,'data2':data2,'data3':data3,'name':name,'data4':data4})

# def ap(request):
#     data5=lawyer_info.objects.all()
#     unique_courts = set()
#     unique_expertise = set()
#     for lawyer in data5:
#         # Split the lexp string by commas and add each value to the unique_expertise set
#         expertise = lawyer.lexp.split(',')
#         unique_expertise.update(expertise)
#     # Filter law objects based on unique expertise values
#     data4 = law.objects.filter(name__in=unique_expertise)
#     for lawyer in data5:
#         # Split the lcourt string by commas and add each value to the unique_courts set
#         courts = lawyer.lcourt.split(',')
#         unique_courts.update(courts)
#
#         # Filter law objects based on unique court names
#     data3 = Court.objects.filter(court_name__in=unique_courts)
#     if request.POST:
#         name=request.POST['aname']
#         acontact = request.POST['acontact']
#         aemail = request.POST['aemail']
#         adate = request.POST['adate']
#         atime = request.POST['atime']
#         amsg = request.POST['amsg']
#         obj=appointment(aname=name,acontact=acontact,aemail=aemail,adate=adate,atime=atime,amsg=amsg)
#         obj.save()
#         return redirect('/ap')
#     return render(request,'myapp/appointment.html',{'data3':data3,'data4':data4})

def case_de(request,id):
    data5 = lawyer_info.objects.all()
    data=case_desc.objects.get(id=id)
    data3 = Court.objects.all()
    unique_expertise = set()
    for lawyer in data5:
        # Split the lexp string by commas and add each value to the unique_expertise set
        expertise = lawyer.lexp.split(',')
        unique_expertise.update(expertise)
    # Filter law objects based on unique expertise values
    data4 = law.objects.filter(name__in=unique_expertise)
    return render(request,'myapp/case_de.html',{'data':data,'data3':data3,'data4':data4})

# def civil_law(request):
#     data = lawyer_info.objects.filter(lexp__icontains='civil law')
#     return render(request,'civil_law.html',{'data':data})

def generate_pdf(request, id):
    # Fetch case data by ID
    case = get_object_or_404(case_desc, id=id)

    # Prepare data to pass to the template
    data = {
        'case_title': case.case_title,
        'case_intro': case.case_intro,
        'case_challenge': case.case_challenge,
        'case_result': case.case_result,
        # Add other fields as needed
    }

    # Render HTML content from template and data
    html_content = render_to_string('myapp/case_de.html', {'data': data})

    # Generate PDF using ReportLab
    pdf_bytes = generate_report(html_content)  # Pass only the HTML content here

    # Return PDF as response
    filename = f"case_study_{id}.pdf"
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
def generate_report(html_content):
    # Parse HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract case title from HTML
    case_title = soup.find('div', class_='section-header').find('h2').text  # Assuming case title is wrapped in an h2 tag

    # Extract main content from HTML
    main_content = soup.find('div', class_='about-text')  # Adjust the class name as per your HTML structure

    # Create a PDF document
    response = HttpResponse(content_type='application/pdf')
    doc = SimpleDocTemplate(response, pagesize=letter)
    styles = getSampleStyleSheet()

    # Define styles for headings
    title_style = styles['Heading1']
    title_style.alignment = TA_CENTER  # Set alignment to center
    content_style = styles['Normal']


    # Define ParagraphStyle for case title
    case_title_style = ParagraphStyle(
        'CaseTitle', parent=title_style, alignment=TA_CENTER
    )

    # Define ParagraphStyle for headings in content
    content_heading_style = ParagraphStyle(
        'ContentHeading', parent=title_style
    )

    # Extract and add Case Title
    paragraphs = []
    paragraphs.append(Paragraph(case_title, case_title_style))  # Add case title

    # Extract and add Introduction section
    paragraphs.append(Paragraph("Introduction", content_heading_style))
    introduction_content = main_content.find('h4', text="Introduction").find_next('p').get_text()
    paragraphs.append(Paragraph(introduction_content, content_style))

    # Extract and add Challenges section
    paragraphs.append(Paragraph("Challenges", content_heading_style))
    challenges_content = main_content.find('h4', text="Challenges").find_next('p').get_text()
    paragraphs.append(Paragraph(challenges_content, content_style))

    # Extract and add Conclusion section
    paragraphs.append(Paragraph("Conclusion", content_heading_style))
    conclusion_content = main_content.find('h4', text="Conclusion").find_next('p').get_text()
    paragraphs.append(Paragraph(conclusion_content, content_style))

    # Add paragraphs to the PDF document
    doc.build(paragraphs)

    # Return the PDF content
    return response.content


def payment(request):
    # Razorpay KeyId and key Secret
    key_id = 'rzp_test_PvM4GxK9MYlCUc'
    key_secret = 'WzsOTRAU4l3oAA1CS7jlVS5E'
    # price=request.POST.get('price')
    amount = int("500") * 100
    client = razorpay.Client(auth=(key_id, key_secret))
    data = {

        'amount': amount,
        'currency': 'INR',
        "receipt": "Client Appointment",
        "notes": {
            'name': 'Online Advocate Management',
            'payment_for': 'Client Appointment'
        }
    }
    result = 1
    payment = client.order.create(data=data)
    context = {'payment': payment, 'result': result}
    return render(request, 'myapp/payment.html', context)

@csrf_exempt
def success(request):
    context = {}
    return render(request, 'myapp/success_payment.html', context)


def ap(request):
    data5=lawyer_info.objects.all()
    unique_courts = set()
    unique_expertise = set()
    for lawyer in data5:
        # Split the lexp string by commas and add each value to the unique_expertise set
        expertise = lawyer.lexp.split(',')
        unique_expertise.update(expertise)
    # Filter law objects based on unique expertise values
    data4 = law.objects.filter(name__in=unique_expertise)
    for lawyer in data5:
        # Split the lcourt string by commas and add each value to the unique_courts set
        courts = lawyer.lcourt.split(',')
        unique_courts.update(courts)

        # Filter law objects based on unique court names
    data3 = Court.objects.filter(court_name__in=unique_courts)
    if request.POST:
        name=request.POST['aname']
        acontact = request.POST['acontact']
        aemail = request.POST['aemail']
        adate = request.POST['adate']
        atime = request.POST['atime']
        amsg = request.POST['amsg']
        obj=appointment(aname=name,acontact=acontact,aemail=aemail,adate=adate,atime=atime,amsg=amsg)
        obj.save()
        subject = 'Appointment Confirmation Meet Link'
        videocallem = "Thank you for Using Appointment Services on Online Advocate Management" + "\n" + "\n" + "\n" + "Here is your Link for videocall:"  + "https://meet.jit.si/client_appointment"+"\n" + "\n" + "\n"+f'Time is : {atime}'+"\n" + "\n" + "\n"+f"Date is : {adate}"
        message=videocallem
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [aemail, 'kushaltrivedi82@gmail.com']
        send_mail(subject, message, email_from, recipient_list)
        return redirect('/#')
    return render(request,'myapp/appointment.html',{'data3':data3,'data4':data4})
