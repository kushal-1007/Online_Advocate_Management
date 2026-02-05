import pycountry
from django.shortcuts import render, redirect, get_object_or_404

from adminapp.models import adminrecord
from clientapp.models import signup, plan, Order
from lawyerapp.models import review
from myapp.models import contactus, appointment, lawyer_info, case_study, blog, case_desc, client_info, Court, law


def index(request):
    data = lawyer_info.objects.count()
    data1 = appointment.objects.count()
    data2 = contactus.objects.count()
    data3 = client_info.objects.count()
    data4 = review.objects.count()
    return render(request, 'admin/index.html',
                  {'data': data, 'data1': data1, 'data2': data2, 'data3': data3, 'data4': data4})


def register(request):
    lawyer_names = lawyer_info.objects.values_list('lname', flat=True)

    # Get the subdivisions (states) for India
    india_states = pycountry.subdivisions.get(country_code='IN')

    # Extract the state names from the subdivisions
    state_names = [state.name for state in india_states]
    if request.POST:
        name = request.POST['name']
        email = request.POST['email']
        country = request.POST['country']
        lawyer = request.POST['lawyer']
        contact = request.POST['phone']
        i = request.FILES['img']
        password = request.POST['password']
        obj = signup(name=name, email=email, country=country, password=password, phone=contact, img=i, lawyer=lawyer)
        obj.save()
        return redirect('/adminapp/index')
    return render(request, 'admin/register.html', {'lawyer_names': lawyer_names, "states": state_names})


def sign(request):
    if request.POST:
        email = request.POST['email']
        password = request.POST['password']
        count = adminrecord.objects.filter(aemail=email, apassword=password).count()
        if count > 0:
            return redirect('/adminapp/index')
    return render(request, 'admin/signin.html')


def show_1(request):
    data = contactus.objects.all
    return render(request, 'admin/show_1.html', {'data': data})


def lawyer_show(request):
    data = lawyer_info.objects.all
    return render(request, 'admin/lawyer_show.html', {'data': data})


def show_appointment(request):
    data = appointment.objects.all
    return render(request, 'admin/appointment.html', {'data': data})


# def update_ap(request, id):
#     data = appointment.objects.get(id=id)
#     if request.POST:
#         name = request.POST['aname']
#         acontact = request.POST['acontact']
#         aemail = request.POST['aemail']
#         adate = request.POST['adate']
#         atime = request.POST['atime']
#         amsg = request.POST['amsg']
#         obj = appointment(aname=name, acontact=acontact, aemail=aemail, adate=adate, atime=atime, amsg=amsg, id=id)
#         obj.save()
#         return redirect('/show_ap')
#     return render(request, 'admin/update_appointment.html', {'data': data})


# def delete_ap(request, id):
#     appointment.objects.get(id=id).delete()
#     return redirect('/show_ap')


def updatecase(request, id):
    data = case_study.objects.get(pk=id)
    data1 = case_desc.objects.get(pk=id)
    data2=law.objects.all()
    selected_case = data.case
    if request.POST:
        title = request.POST['title']
        a = request.POST.get('selected_case')
        category = request.POST['case_type']
        ctime = request.POST['ctime']
        intro = request.POST['case_intro']
        challenge = request.POST['case_challenge']
        result = request.POST['case_result']
        data.title = title
        data.case = a
        data.case_type = category
        data.ctime = ctime
        data1.case_intro = intro
        data1.case_challenge = challenge
        data1.case_result = result
        if len(request.FILES) != 0:
            data.case_img = request.FILES['cimg']
        data.save()
        data1.save()
        return redirect('/adminapp/case_1')
    return render(request, 'admin/updateCaseStudy.html', {'data': data, 'data1': data1, 'data2': data2,
                                                          'selected_case': selected_case})
    # else:
    #     selected_case = data.case
    #     return render(request, 'admin/updateCaseStudy.html', {'data': data, 'data1': data1,'data2':data2,
    #                                                           'selected_case':selected_case})


def case_1(request):
    data = case_study.objects.all
    return render(request, 'admin/case_study.html', {'data': data})


def deletecase(request, id):
    case_study.objects.get(id=id).delete()
    case_desc.objects.get(id=id).delete()
    return redirect('/adminapp/index')


def addlawyer(request):
    data1 = Court.objects.all()  # Fetch all courts
    data2=law.objects.all()
    india_states = pycountry.subdivisions.get(country_code='IN')

    # Extract the state names from the subdivisions
    state_names = [state.name for state in india_states]

    # Optionally, you can sort the state names alphabetically
    state_names.sort()

    if request.method == 'POST':
        name = request.POST.get('lname')
        contact = request.POST.get('lcontact')
        profession = request.POST.get('lprofession')
        selected_court_name = request.POST.get('selected_court')  # Get the selected court's name
        experience = request.POST.get('lexperience')
        email = request.POST.get('lemail')
        state = request.POST.get('lstate')
        image = request.FILES.get('limg')
        expert = request.POST.getlist('expert')
        password = request.POST.get('lpassword')

        # Create lawyer_info object
        data = lawyer_info.objects.create(
            lname=name,
            lcontact=contact,
            lprofession=profession,
            lcourt=selected_court_name,  # Assign the selected court's name
            lexperience=experience,
            lstate=state,
            lemail=email,
            limg=image,
            lexp=','.join(expert),
            lpassword=password
        )
        return redirect('/adminapp/index')
    # else:
    #     choices_tuples = lawyer_info.EXPERTISE_CHOICE
    #     all_expert = [choice[1] for choice in choices_tuples]
    return render(request, 'admin/lawyer_form.html',
                      {'data2': data2, 'data1': data1, 'states': state_names})


# def addlawyer(request):
#     # data1=lawyer_info.objects.all()
#     # data1 = lawyer_info.objects.values_list('lcourt', flat=True).distinct()
#     data1=Court.objects.all()
#     india_states = pycountry.subdivisions.get(country_code='IN')
#
#     # Extract the state names from the subdivisions
#     state_names = [state.name for state in india_states]
#
#     # Optionally, you can sort the state names alphabetically
#     state_names.sort()
#
#
#     if request.method == 'POST':
#
#         name = request.POST['lname']
#         contact = request.POST['lcontact']
#         profession = request.POST['lprofession']
#         court = request.POST.get('selected_court')
#         experience = request.POST['lexperience']
#         email=request.POST['lemail']
#         state = request.POST['lstate']
#         image = request.FILES['limg']
#         expert = request.POST.getlist('expert')
#         password=request.POST['lpassword']
#
#
#         data = lawyer_info.objects.create(
#             lname=name,
#             lcontact=contact,
#             lprofession=profession,
#             lcourt=court,
#             lexperience=experience,
#             lstate=state,
#             lemail=email,
#             limg=image,
#             lexp=','.join(expert),
#             lpassword=password
#         )
#         return redirect('/adminapp/index')
#     else:
#         choices_tuples = lawyer_info.EXPERTISE_CHOICE
#         all_expert = [choice[1] for choice in choices_tuples]
#         # all_court=lawyer_info.objects.
#         # choices_court = lawyer_info.COURT_CHOICE
#         # all_court = [choice[1] for choice in choices_court]
#         return render(request, 'admin/lawyer_form.html', {'all_expert':all_expert,'data1':data1,'states': state_names})

def updatelawyer(request, id):
    data = get_object_or_404(lawyer_info, pk=id)
    data1 = Court.objects.all()
    data2 = law.objects.all()

    # Get the subdivisions (states) for India
    india_states = pycountry.subdivisions.get(country_code='IN')

    # Extract the state names from the subdivisions
    state_names = [state.name for state in india_states]
    state_names.sort()

    if request.method == 'POST':
        name = request.POST['lname']
        contact = request.POST['lcontact']
        profession = request.POST['lprofession']
        selected_court = request.POST.get('selected_court')
        experience = request.POST['lexperience']
        email = request.POST['lemail']
        state = request.POST['lstate']
        password = request.POST['lpassword']
        expert = request.POST.getlist('expert')

        data.lname = name
        data.lcontact = contact
        data.lprofession = profession
        data.lcourt = selected_court
        data.lexperience = experience
        data.lstate = state
        data.lpassword = password
        data.lemail = email
        data.lexp = ','.join(expert)

        if len(request.FILES) != 0:
            data.limg = request.FILES['limg']

        data.save()
        return redirect('/adminapp/lawyer_show')
    else:
        selected_expert = data.lexp.split(',') if data.lexp else []
        selected_court = data.lcourt

        return render(request, 'admin/update_lawyer.html', {
            'data': data,
            'data2': data2,
            'selected_expert': selected_expert,
            'data1': data1,
            'selected_court': selected_court,
            'states': state_names
        })

# def updatelawyer(request, id):
#     data = get_object_or_404(lawyer_info, pk=id)
#     data1 = Court.objects.all()
#     data2=law.objects.all()
#     # Get the subdivisions (states) for India
#     india_states = pycountry.subdivisions.get(country_code='IN')
#
#     # Extract the state names from the subdivisions
#     state_names = [state.name for state in india_states]
#     state_names.sort()
#     if request.method == 'POST':
#
#         name = request.POST['lname']
#         contact = request.POST['lcontact']
#         profession = request.POST['lprofession']
#         selected_court = request.POST.get('selected_court')
#         experience = request.POST['lexperience']
#         email = request.POST['lemail']
#         state = request.POST['lstate']
#         # image = request.FILES['limg']
#         expert = request.POST.getlist('expert')
#         password = request.POST['lpassword']
#         data.lname = name
#         data.lcontact = contact
#         data.lprofession = profession
#         data.lcourt = selected_court
#         data.lexperience = experience
#         data.lstate = state
#         data.lpassword = password
#         data.lemail = email
#         data.lexp = ','.join(expert)
#         if len(request.FILES) != 0:
#             data.limg = request.FILES['limg']
#
#         data.save()
#         return redirect('/adminapp/lawyer_show')
#     else:
#         # choices_tuples = lawyer_info.lexp
#         # all_expert = [choice[1] for choice in choices_tuples]
#         selected_expert = data.lexp.split(',') if data.lexp else []
#         # all_court = [choice[1] for choice in lawyer_info.COURT_CHOICE]
#         selected_court = data.lcourt
#
#     return render(request, 'admin/update_lawyer.html',
#                   {'data': data, 'data2': data2, 'selected_expert': selected_expert, 'data1': data1,
#                    'selected_court': selected_court, 'states': state_names})


def deletelawyer(request, id):
    lawyer_info.objects.get(id=id).delete()
    return redirect('/adminapp/lawyer_show')


def blog_form(request):
    data=law.objects.all()
    if request.method == 'POST':
        title = request.POST['btitle']
        type = request.POST['selected_blog']
        time = request.POST['btime']
        desc = request.POST['bdesc']
        image = request.FILES['bimg']
        data = blog.objects.create(
            btitle=title,
            bimg=image,
            btype=type,
            btime=time,
            bdesc=desc
        )
        return redirect('/adminapp/blog_show')
    # else:
    #     choices_tuples = blog.BLOG_CHOICE
    #     all_blog = [choice[1] for choice in choices_tuples]
    return render(request, 'admin/blog_form.html', {'data': data})


def addCase(request):
    data2=law.objects.all()
    if request.POST:
        title = request.POST['title']
        # type = request.POST['case']
        type = request.POST.get('selected_case')
        category = request.POST['case_type']
        ctime = request.POST['ctime']
        cimg = request.FILES['case_img']
        intro = request.POST['case_intro']
        challenge = request.POST['case_challenge']
        result = request.POST['case_result']
        obj1 = case_study(title=title, case=type, case_type=category, ctime=ctime, case_img=cimg)
        obj2 = case_desc(case_title=title, case_intro=intro, case_challenge=challenge, case_result=result)
        obj1.save()
        obj2.save()
        return redirect('/adminapp/index')
    return render(request, 'admin/addCaseStudy.html',{'data2':data2})


def blog_show(request):
    data = blog.objects.all
    return render(request, 'admin/blog_show.html', {'data': data})


def updateblog(request, id):
    data = get_object_or_404(blog, pk=id)
    data1=law.objects.all()
    if request.method == 'POST':
        title = request.POST['btitle']
        type = request.POST['selected_blog']
        time = request.POST['btime']
        desc = request.POST['bdesc']
        data.btitle = title
        data.btype = type
        data.btime = time
        data.bdesc = desc
        if len(request.FILES) != 0:
            data.bimg = request.FILES['bimg']
        data.save()
        return redirect('/adminapp/index')
    else:
        # all_blog = [choice[1] for choice in blog.BLOG_CHOICE]
        selected_blog = data.btype

    return render(request, 'admin/updateBlog.html',
                  {'data': data, 'data1': data1, 'selected_blog': selected_blog})


def deleteBlog(request, id):
    blog.objects.get(id=id).delete()
    return redirect('/adminapp/blog_show')


def showlawyerfeedback(request):
    data = review.objects.all
    return render(request, 'admin/feedback_lawyer_show.html', {'data': data})


def showclientfeedback(request):
    data = client_info.objects.all
    return render(request, 'admin/showclientfeedback.html', {'data': data})


def showclient(request):
    # data=client_info.objects.all
    data = signup.objects.all
    return render(request, 'admin/client_show.html', {'data': data})


def updateclient(request, id):
    data = signup.objects.get(id=id)
    all_lawyer_names = lawyer_info.objects.values_list('lname', flat=True).distinct()
    india_states = pycountry.subdivisions.get(country_code='IN')
    state_names = [state.name for state in india_states]
    state_names.sort()
    selected_lawyer_name = data.lawyer
    if request.POST:
        name = request.POST['name']
        password = request.POST['password']
        email = request.POST['email']
        country = request.POST['country']
        lawyer = request.POST['lawyer']
        contact = request.POST['phone']
        if len(request.FILES) != 0:
            data.img = request.FILES['img']

        data.name = name
        data.password = password
        data.email = email
        data.country = country
        data.lawyer = lawyer
        data.phone = contact
        # obj = signup(id=id,name=name, email=email, country=country, password=password, phone=contact, img=i, lawyer=lawyer)
        data.save()
        return redirect('/adminapp/index')
    return render(request, 'admin/update_client.html',
                  {'data': data, 'selected_lawyer_name': selected_lawyer_name, 'all_lawyer_names': all_lawyer_names,
                   'states': state_names})


def deleteclient(request, id):
    signup.objects.get(id=id).delete()
    return redirect('/adminapp/index')


def addCourt(request):
    if request.method == 'POST':
        court_name = request.POST.get('court')
        desc = request.POST.get('desc')

        # Check if a court with the same name already exists
        existing_court = Court.objects.filter(court_name=court_name).first()
        if existing_court:
            # Court with the same name already exists, append the new description
            existing_court.desc += ' ' + desc  # Append the new description with a newline
            existing_court.save()
        else:
            # Create and save the new court
            obj = Court(court_name=court_name, desc=desc)
            obj.save()

        return redirect('/adminapp/addCourt')  # Redirect to the same page after successful addition

    return render(request, 'admin/court.html')
# def addCourt(request):
#     if request.POST:
#         court1 = request.POST['court']
#         desc1 = request.POST['desc']
#         obj = Court(court_name=court1, desc=desc1)
#         obj.save()
#         return redirect('/adminapp/addCourt')
#     return render(request, 'admin/court.html')


def updateCourt(request, id):
    data = Court.objects.get(id=id)
    if request.POST:
        court1 = request.POST['court']
        desc1 = request.POST['desc']
        obj = Court(court_name=court1, desc=desc1)
        obj.save()
        return redirect('/adminapp/showCourt')
    return render(request, 'admin/updateCourt.html', {'data': data})


def deleteCourt(request, id):
    Court.objects.get(id=id).delete()
    return redirect('/adminapp/showCourt')


def showCourt(request):
    data = Court.objects.all
    return render(request, 'admin/showCourt.html', {'data': data})


def addLaw(request):
    if request.method == 'POST':
        law_name = request.POST.get('law_name')
        law_def = request.POST.get('law_def')
        law_desc = request.POST.get('law_desc')

        # Check if a law with the same name already exists
        existing_law = law.objects.filter(name=law_name).first()
        if existing_law:
            # Law with the same name already exists, append the new definition and description
            existing_law.definition += ' ' + law_def  # Append the new definition with a newline
            existing_law.law_desc += ' ' + law_desc  # Append the new description with a newline
            existing_law.save()
        else:
            # Create and save the new law
            obj = law(name=law_name, definition=law_def, law_desc=law_desc)
            obj.save()

        return redirect('/adminapp/index')

    return render(request, 'admin/addLaw.html')
# def addLaw(request):
#     if request.POST:
#         law_name=request.POST['law_name']
#         law_def=request.POST['law_def']
#         law_desc=request.POST['law_desc']
#         obj=law(name=law_name,definition=law_def,law_desc=law_desc)
#         obj.save()
#         return redirect('/adminapp/index')
#     return render(request,'admin/addLaw.html')

def updateLaw(request,id):
    data=law.objects.get(id=id)
    if request.POST:
        law_name = request.POST['law_name']
        law_def = request.POST['law_def']
        law_desc = request.POST['law_desc']
        obj = law(id=id,name=law_name, definition=law_def, law_desc=law_desc)
        obj.save()
        return redirect('/adminapp/show_law')
    return render(request, 'admin/updatelaw.html',{'data':data})

def deleteLaw(request,id):
    law.objects.get(id=id).delete()
    return redirect('/adminapp/show_law')

def show_law(request):
    data=law.objects.all()
    return render(request,'admin/showLaw.html',{'data':data})


def price_plan(request):
    if request.POST:
        n=request.POST['name']
        p=request.POST['price']
        d1=request.POST['d1']
        d2 = request.POST['d2']
        d3 = request.POST['d3']
        d4 = request.POST['d4']
        d5 = request.POST['d5']
        obj=plan(name=n,price=p,d1=d1,d2=d2,d3=d3,d4=d4,d5=d5)
        obj.save()
        return redirect('/adminapp/index')
    return render(request,'admin/price_plan.html')

def update_plan(request,id):
    data=plan.objects.get(id=id)
    if request.POST:
        n=request.POST['name']
        p=request.POST['price']
        d1=request.POST['d1']
        d2 = request.POST['d2']
        d3 = request.POST['d3']
        d4 = request.POST['d4']
        d5 = request.POST['d5']
        obj=plan(id=id,name=n,price=p,d1=d1,d2=d2,d3=d3,d4=d4,d5=d5)
        obj.save()
        return redirect('/adminapp/index')
    return render(request,'admin/update_plan.html',{'data':data})

def delete_plan(request,id):
    plan.objects.get(id=id).delete()
    return redirect('/adminapp/showplan')

def showplan(request):
    data=plan.objects.all()
    return render(request,'admin/show_pricing_plan.html',{'data':data})

def showpayment(request):
    data=Order.objects.all()
    # data = signup.objects.filter(order__payment_status='success')
    return render(request,'admin/show_payment_details.html',{'data':data})