import datetime
import random
import string

from django.contrib.admin.models import LogEntry
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Q, Prefetch
from django.http import HttpResponse, HttpResponseRedirect, request
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.
from django.template import loader
from django.urls import reverse

from .models import Account, Pricing, PaymentHistory
from django.conf import settings

from ..book.models import Receipt
from ..loan.models import loanStatus


def login_user(request):
    if request.method == "POST":
        username = request.POST['adminUsername']
        password = request.POST['adminPassword']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            current_user = request.user
            login(request, user)
            is_staff = request.user.is_staff
            is_banned = request.user.is_banned
            if is_staff is True and is_banned is False:
                request.session['name'] = current_user.name
                request.session['id'] = current_user.id
                # request.session['image'] = current_user.profile_image
                messages.success(request, 'Hello ' + request.session['name'] + ', Welcome Back !!!')
                return redirect('indexOfAdmin')
            else:
                logout(request)
                messages.success(request, "You don't have permission to login to this page !!!")
                return redirect('LogInAdmin')
        else:
            messages.success(request, 'Wrong Username Or Password !!!')
            return redirect('LogInAdmin')
    else:
        return render(request, 'misc/authentication/login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, "See You Soon !!")
    return redirect('LogInAdmin')


@login_required
def userIndex(request):
    today = datetime.date.today()
    end = today + datetime.timedelta(7)
    nearends = Account.objects.filter(is_admin=False, is_staff=False, is_superuser=False,expired_date__lte=end,is_banned=False)
    accounts = Account.objects.filter(is_admin=False, is_staff=False, is_superuser=False)
    template = loader.get_template('users/index.html')
    pricing = Pricing.objects.all().order_by('pricing_price')
    def accountCounter():
        count = Account.objects.filter(is_admin=False, is_staff=False, is_superuser=False).count()
        return count

    currentlyOnline = Account.objects.filter(is_active=True).count()
    x = accountCounter()
    y = nearends.count()
    context = {
        'nearends' : nearends,
        'accounts': accounts,
        'currentlyOnline': currentlyOnline,
        'media_url': settings.MEDIA_URL,
        'x': x,
        'y':y,
        'pricing':pricing
    }
    # str(authors.query)
    return HttpResponse(template.render(context, request))


@login_required
def add(request):
    template = loader.get_template('users/add.html')
    return HttpResponse(template.render({}, request))


@login_required
def addUser(request):
    def randomUsername():
        source = string.ascii_letters + string.digits
        result_str = 'HL' + ''.join((random.choice(source) for i in range(8)))
        return result_str

    def randomPassword():
        source = string.ascii_letters + string.digits
        result_str = ''.join((random.choice(source) for i in range(12)))
        return result_str

    email = request.POST['email']
    username = randomUsername()
    password = randomPassword()
    name = request.POST['name']
    phone_number = request.POST['phone_number']
    address = request.POST['address']
    birth_date = request.POST['birth_date']
    expired_date = request.POST['expired_date']
    national_id = request.POST['national_id']
    image = request.FILES.get('user_image')
    date_joined = datetime.datetime.now
    created_by = Account.objects.get(id=request.session['id'])
    if image is None:
        Account.objects.create_user(email=email,
                                    username=username,
                                    password=password,
                                    name=name,
                                    date_joined=date_joined,
                                    phone_number=phone_number,
                                    address=address,
                                    birth_date=birth_date,
                                    expired_date=expired_date,
                                    national_id=national_id,
                                    profile_image='NULL',
                                    created_by=created_by.id)
    else:
        Account.objects.create_user(email=email,
                                    username=username,
                                    password=password,
                                    name=name,
                                    date_joined=date_joined,
                                    phone_number=phone_number,
                                    address=address,
                                    birth_date=birth_date,
                                    expired_date=expired_date,
                                    national_id=national_id,
                                    profile_image=image,
                                    created_by=created_by.id)
    subject = 'Welcome to HiusLibrary'
    message = f'Hi {name}, thank you for registering in HiusLibrary. \n' \
              f'This is your Access Key and Password for www.hiuslibrary.vn \n' \
              f'Please do not share this information with anyone. \n' \
              f'Access Key: {username} \n' \
              f'Password: {password} \n' \
              f'\t\t\t Sincerely, \n' \
              f'\t\t\t {created_by.name}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]
    send_mail(subject, message, email_from, recipient_list)
    messages.success(request, "The user is successfully registered !!!")
    return HttpResponseRedirect(reverse('userIndex'))


@login_required
def adminIndex(request):
    accounts = Account.objects.filter(is_staff=True,is_superuser=False)
    template = loader.get_template('administrator/index.html')

    def accountCounter():
        count = Account.objects.filter(is_staff=True).count()
        return count

    x = accountCounter()
    context = {
        'accounts': accounts,
        'x': x,
    }
    # str(authors.query)
    return HttpResponse(template.render(context, request))


@login_required
def updateProfile(request):
    user = Account.objects.get(id=request.session['id'])
    createdBy = Account.objects.filter(created_by=request.session['id']).prefetch_related(
        Prefetch('user_created_by', Account.objects.filter(created_by=request.session['id']))).order_by('date_joined')[:5][::-1]
    counter = Account.objects.filter(created_by=request.session['id']).prefetch_related(
        Prefetch('user_created_by', Account.objects.filter(created_by=request.session['id']))).count()
    activities = LogEntry.objects.filter(user_id = request.session['id']).order_by('-action_time')[:10]
    template = loader.get_template('administrator/update_profile.html')
    context = {
        'user': user,
        'activities':activities,
        'counter': counter,
        'createdBy': createdBy,
        'media_url': settings.MEDIA_URL,
    }
    # str(authors.query)
    return HttpResponse(template.render(context, request))


@login_required
def info(request, id):
    user = Account.objects.filter(Q(is_staff=True) | Q(is_admin=True) | Q(is_superuser=True)).get(id=id)
    template = loader.get_template('administrator/info.html')
    createdBy = Account.objects.filter(created_by=id).prefetch_related(
        Prefetch('user_created_by', Account.objects.filter(created_by=id))).order_by('date_joined')[:5][::-1]
    counter = Account.objects.filter(created_by=id).prefetch_related(
        Prefetch('user_created_by', Account.objects.filter(created_by=id))).count()
    activities = LogEntry.objects.filter(user_id = id).order_by('-action_time')[:10]
    a = request.session['id']
    context = {
        'user': user,
        'a': a,
        'counter': counter,
        'activities':activities,
        'media_url': settings.MEDIA_URL,
        'createdBy': createdBy
    }
    return HttpResponse(template.render(context, request))


@login_required
def extendMembership(request):
    data = request.GET['catid']
    user = Account.objects.get(id=data)
    user.expired_date = user.expired_date + datetime.timedelta(seconds=1 * 31 * 24 * 60 * 60)
    user.save()
    payment = PaymentHistory(
        user_id = user,
        pricing = Pricing.objects.get(pricing_id=2),
        old_expired_date = user.expired_date,
        new_expired_date = user.expired_date + datetime.timedelta(days=31)
    )
    payment.save()
    return HttpResponseRedirect(reverse('userIndex'))


@login_required
def banUser(request):
    data = request.GET['catid']
    admin = Account.objects.get(id=request.session['id'])
    user = Account.objects.get(id=data)
    if user.is_banned is True:
        user.is_banned = False
    elif user.is_banned is False:
        user.is_banned = True
        user.expired_date = datetime.datetime.today()
        user.banned_by = admin
    user.save()
    return HttpResponseRedirect(reverse('userIndex'))


@login_required
def addAdmin(request):
    template = loader.get_template('administrator/add.html')
    return HttpResponse(template.render({}, request))


@login_required
def addAdminProccess(request):
    name = request.POST['name']
    username = request.POST['username']
    email = request.POST['email']
    birth_date = request.POST['birth_date']
    password = request.POST['password']
    national_id = request.POST['national_id']
    adminRole = request.POST['adminRole']
    phone_number = request.POST['phone_number']
    address = request.POST['address']
    created_by = Account.objects.get(id=request.session['id'])
    date_joined = datetime.datetime.now
    Account.objects.create_staff(email=email,
                                 username=username,
                                 password=password,
                                 name=name,
                                 date_joined=date_joined,
                                 phone_number=phone_number,
                                 address=address,
                                 birth_date=birth_date,
                                 national_id=national_id,
                                 is_admin=adminRole,
                                 is_staff=True,
                                 profile_image='NULL',
                                 created_by=created_by.id
                                 )
    messages.success(request, "The user is successfully registered !!!")
    return HttpResponseRedirect(reverse('adminIndex'))
def loginForUser(request):
    if request.method == "POST":
        username = request.POST['userkey']
        password = request.POST['userpassword']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            current_user = request.user
            login(request, user)
            is_banned = request.user.is_banned
            if is_banned is False:
                request.session['name'] = current_user.name
                request.session['id'] = current_user.id
                # request.session['image'] = current_user.profile_image
                messages.success(request, 'Hello ' + request.session['name'] + ', Welcome Back !!!')
                return redirect('indexOfUser')
            else:
                logout(request)
                messages.success(request, "You don't have permission to login to this page !!!")
                return redirect('indexOfUser')
        else:
            messages.success(request, 'Wrong Username Or Password !!!')
            return redirect('indexOfUser')
    else:
        return render(request, 'indexOfUser', {})


def logoutForUser(request):
    logout(request)
    messages.success(request, "See You Soon !!")
    return HttpResponseRedirect(reverse('indexOfUser'))

@login_required
def historyAdmin(request):
    all = PaymentHistory.objects.all().prefetch_related().order_by('-history_Id')
    x = all.count()
    context = {
        'all' :all,
        'x': x
    }
    template = loader.get_template('history/index.html')
    return HttpResponse(template.render(context, request))
@login_required
def bookUser(request,id):
    loans = loanStatus.objects.all()
    user = Account.objects.get(id = id)
    payments = PaymentHistory.objects.prefetch_related().filter(user_id=id).order_by('-history_Id')
    y = payments.count()
    receipts = Receipt.objects.prefetch_related().filter(receipt_user=id).order_by('-receipt_id')
    x = receipts.count()
    context = {
        'x': x,
        'y':y,
        'user': user,
        'loans': loans,
        'receipts': receipts,
        'payments': payments
    }
    template = loader.get_template('books/bookUser.html')
    return HttpResponse(template.render(context, request))
@login_required
def profileUpdate(request):
    name = request.POST['adminName']
    email = request.POST['adminEmail']
    phone = request.POST['adminPhone']
    birthDate = request.POST['adminDoB']
    address = request.POST['adminAddress']
    linkedIn = request.POST['adminLinkedIn']
    twitter = request.POST['adminTwitter']
    instagram = request.POST['adminInstagram']
    facebook = request.POST['adminFacebook']
    image = request.FILES.get('image')
    user = Account.objects.get(id=request.session['id'])
    if image is None:
        user.name = name
        user.email = email
        user.phone = phone
        user.birth_date = birthDate
        user.address = address
        user.linkedIn = linkedIn
        user.twitter = twitter
        user.instagram = instagram
        user.facebook = facebook
    else:
        user.name = name
        user.email = email
        user.phone = phone
        user.birth_date = birthDate
        user.address = address
        user.linkedIn = linkedIn
        user.twitter = twitter
        user.instagram = instagram
        user.facebook = facebook
        user.profile_image = image
    user.save()
    return redirect('updateProfile')
@login_required
def lockAdmin(request,id):
    user = Account.objects.get(id = id)
    if user.is_banned is True :
        user.is_banned = False
        user.banned_by = None
    else:
        user.is_banned = True
        user.banned_by = Account.objects.get(id=request.session['id'])
        user.expired_date = datetime.date.today()
    user.save()
    return redirect('adminIndex')
@login_required
def promoteAdmin(request,id):
    user = Account.objects.get(id=id)
    if user.is_admin is True:
        user.is_admin = False
    else:
        user.is_admin = True
    user.save()
    return redirect('adminIndex')
@login_required
def extendManual(request,id):
    strid = str(id)
    price = request.POST['price' + strid]
    user = Account.objects.get(id = id)
    pricing = Pricing.objects.get(pricing_id = price)
    days = pricing.pricing_days
    paymentHistory = PaymentHistory(
        pricing_id = price,
        user_id = user,
        old_expired_date = user.expired_date,
        new_expired_date  = user.expired_date + datetime.timedelta(days=days)
    )
    paymentHistory.save()
    user.expired_date = user.expired_date + datetime.timedelta(days=days)
    user.save()
    return redirect('userIndex')
@login_required
def adminLog(request,id):
    strid = str(id)
    logs = LogEntry.objects.raw('SELECT * FROM django_admin_log INNER JOIN accounts_account ON django_admin_log.user_id = accounts_account.id WHERE content_type_id = '+ strid + ' ORDER BY action_time DESC')
    context={
        'logs':logs
    }
    template = loader.get_template('misc/admin_log.html')
    return HttpResponse(template.render(context, request))
@login_required
def activities(request):
    logs=LogEntry.objects.filter(user_id=request.session['id'])
    context={
        'logs':logs
    }
    template = loader.get_template('misc/activity_log.html')
    return HttpResponse(template.render(context, request))
@login_required
def changePasswordAdmin(request):
    template = loader.get_template('misc/change_password.html')
    return HttpResponse(template.render({}, request))
@login_required
def changePasswordAdminProc(request):
    oldPassword= request.POST['oldPassword']
    newPassword = request.POST['newPassword']
    current_user = Account.objects.get(id = request.session['id'])
    current_user_name = current_user.username
    user = authenticate(username=current_user_name, password=oldPassword)
    if user is not None:
        current_user.set_password(newPassword)
        current_user.save()
        messages.success(request, "Success, Please Log-In to your account again !!!")
        return redirect('indexOfAdmin')
    else:
        messages.success(request, "Password Incorrect !!!")
        return redirect('changePasswordAdmin')