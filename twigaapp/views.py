import json
import os

import requests
from decouple import config
from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from django.http import HttpResponse
from requests.auth import HTTPBasicAuth
from django.shortcuts import render, redirect, get_object_or_404
from twigaapp.forms import BookingForm, ImageUploadForm
from django.contrib.auth.hashers import make_password, check_password
from twigaapp.credentials import MpesaAccessToken, LipanaMpesaPassword
from twigaapp.models import Contacts, Bookings, ImageModels, Users, Managers

def index(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = Users.objects.get(username=username)
            if check_password(password, user.password):
                return render(request, 'index.html')
            else:
                messages.error(request, 'Incorrect password.')
                return render(request, 'login.html', {
                'username': request.POST['username']
                })
        except Users.DoesNotExist:
            messages.error(request, 'User profile not found.')
            return redirect('login')
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'register.html', {
                'username': request.POST['username'],
                'phone': request.POST['phone'],
                'email': request.POST['email']
            })
        hashed_password = make_password(password)
        new_user = Users(
            username=request.POST['username'],
            phone=request.POST['phone'],
            email=request.POST['email'],
            password=hashed_password,
        )
        new_user.save()
        return redirect('/login')
    return render(request, 'register.html')

def login(request):
    return render(request, 'login.html')

# TODO this uses the full page animation with 4 sliders from TULEN we saw?
#  Or keep the default
def services(request):
    return render(request, 'services.html')

def bookings(request):
    return render(request, 'bookings.html')

def menu(request):
    return render(request, 'menu.html')

def about(request):
    return render(request, 'about.html')


def contact(request):
    if request.method == 'POST':
        new_contact = Contacts(
            name=request.POST['name'],
            phone=request.POST['phone'],
            email=request.POST['email'],
            subject=request.POST['subject'],
            message=request.POST['message'],
        )
        new_contact.save()
        return redirect('/contact')
    else:
        return render(request, 'contact.html')


def gallery(request):
    images = ImageModels.objects.all().order_by('-id')
    return render(request, 'gallery.html', {'images': images})

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/gallery#twiga_gallery')
        else:
            return render(request, 'gallery.html', {'form': form})
    else:
        form = ImageUploadForm()
    return render(request, 'gallery.html', {'form': form})

def image_delete(request, id):
    image = ImageModels.objects.get(id=id)
    image.delete()
    return redirect('/gallery#twiga_gallery')


def token(request):
    consumer_key = config('CONSUMER_KEY')
    consumer_secret = config('CONSUMER_SECRET')
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]
    return render(request, 'token.html', {"token": validated_mpesa_access_token})


def pay(request):
    return render(request, 'pay.html')


def stk(request):
    if request.method == "POST":
        phone = request.POST['phone']
        amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "BusinessShortCode": LipanaMpesaPassword.Business_short_code,
            "Password": LipanaMpesaPassword.decode_password,
            "Timestamp": LipanaMpesaPassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "eMobilis",
            "TransactionDesc": "Web Development Charges"
        }
        response = requests.post(api_url, json=request, headers=headers)
        return HttpResponse("Success")


def manager_register(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'twiga_management/register.html', {
                'manager_name': request.POST['manager_name'],
                'phone': request.POST['phone'],
                'email': request.POST['email'],
                'image': request.FILES.get['image']
            })
        new_manager = Managers(
            manager_name=request.POST['manager_name'],
            phone=request.POST['phone'],
            email=request.POST['email'],
            image=request.FILES.get('image', None),
            password=make_password(request.POST['password']),
        )
        new_manager.save()
        return redirect('/manager_login')
    return render(request, 'twiga_management/register.html')


def manager_login(request):
    if request.method == 'POST':
        manager_name = request.POST.get('manager_name')
        password = request.POST.get('password')
        try:
            print("Finding the manager object from the manager field...")
            manager = Managers.objects.get(manager_name=manager_name)
            if check_password(password, manager.password):
                request.session['manager_id'] = manager.id
                request.session.save()
                print("Saving manager_id to session...")
                print(f"Session saved with manager_id: {manager.id}")
                print(f"Session contents: {request.session.items()}")
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid password.')
        except Managers.DoesNotExist:
            messages.error(request, 'Manager not found.')
    return render(request, 'twiga_management/login.html')


def dashboard(request):
    manager_id = request.session.get('manager_id')
    print(f"Retrieved manager_id from session: {manager_id}")
    if not manager_id:
        print('Cannot find manager_id')
        messages.error(request, 'You must be logged in to access the dashboard.')
        return redirect('manager_login')
    # Fetch the logged-in manager's details
    manager = get_object_or_404(Managers, id=manager_id)
    # Retrieve additional data for the dashboard
    all_contacts = Contacts.objects.all().order_by('-id')
    all_users = Users.objects.all().order_by('-id')
    all_managers = Managers.objects.all().order_by('-id')
    total_contacts = Contacts.objects.count()
    duplicate_phones = (
        Contacts.objects.values('phone')
        .annotate(phone_count=Count('phone'))
        .filter(phone_count__gt=1)
    )
    return render(request, 'twiga_management/dashboard.html', {
        'contacts': all_contacts,
        'users': all_users,
        'managers': all_managers,
        'manager': manager,
        'total_contacts': total_contacts,
        'duplicate_phones': duplicate_phones,
    })


def mgr_edit_image(request, manager_id):
    manager = get_object_or_404(Managers, id=manager_id)
    if request.method == 'POST' and request.FILES.get('image'):
        new_image = request.FILES['image']
        if manager.image:
            old_image_path = manager.image.path
            if os.path.exists(old_image_path):
                os.remove(old_image_path)
        manager.image = new_image
        manager.save()
        return redirect('managers')
    return redirect('managers')



def manager_delete(request, id):
    manager = Managers.objects.get(id=id)
    if request.session.get('manager_id') == id:
        if manager.image:
            image_path = manager.image.path
            if os.path.exists(image_path):
                os.remove(image_path)
        logout(request)
        request.session.flush()
        manager.delete()
        return redirect('manager_login')

    manager.delete()
    print(f"Manager {manager.manager_name} (ID: {manager.id}) deleted by another user.")
    return redirect('managers')


def mgr_delete_image(request, manager_id):
    manager = get_object_or_404(Managers, id=manager_id)
    if manager.image:
        old_image_path = manager.image.path
        if os.path.exists(old_image_path):
            os.remove(old_image_path)
    manager.image = None
    manager.save()
    return redirect('managers')


def documentation(request):
    manager_id = request.session.get('manager_id')
    if not manager_id:
        # If no manager_id is found in session, redirect to login page
        print('Cannot find manager_id for documentation.function in views')
        messages.error(request, 'You must be logged in to access the documentation.')
        return redirect('manager_login')
    # Fetch the logged-in manager's details
    manager = Managers.objects.get(id=manager_id)
    # Pass the manager object to the template
    return render(request, 'twiga_management/documentation.html', {
        'manager': manager
    })


def manager_logout(request):
    logout(request)
    return redirect('manager_login')

def users(request):
    manager_id = request.session.get('manager_id')
    if not manager_id:
        print('Cannot find manager_id for users.function in views')
        messages.error(request, 'You must be logged in to access the twiga users.')
        return redirect('manager_login')
    manager = Managers.objects.get(id=manager_id)
    all_users = Users.objects.all().order_by('-id')
    return render(request, 'twiga_management/users.html', {
        'manager': manager,
        'users': all_users
    })

def user_delete(request, id):
    user = Users.objects.get(id = id)
    user.delete()
    return redirect('/users')

def delete_contact(request, id):
    single_contact = Contacts.objects.get(id = id)
    single_contact.delete()
    return redirect('/dashboard')

def managers(request):
    manager_id = request.session.get('manager_id')
    if not manager_id:
        print('Cannot find manager_id for managers.function in views')
        messages.error(request, 'You must be logged in to access the twiga managers.')
        return redirect('manager_login')
    manager = Managers.objects.get(id=manager_id)
    all_managers = Managers.objects.all().order_by('-id')
    return render(request, 'twiga_management/managers.html', {
        'manager': manager,
        'managers': all_managers
    })



# def appointment(request):
#     if request.method == 'POST':
#         my_appointment = Appointment(
#             name=request.POST['name'],
#             email=request.POST['email'],
#             phone=request.POST['phone'],
#             dateTime=request.POST['dateTime'],
#             department=request.POST['department'],
#             doctor=request.POST['doctor'],
#             message=request.POST['message'],
#         )
#         my_appointment.save()
#         return redirect('/show_appointments')
#     else:
#         return render(request, 'appointment.html')
#
# def show_appointments(request):
#     all_appointments = Appointment.objects.all()
#     return render(request, 'showAppointments.html', {'appointments': all_appointments})
#
# def edit_appointment(request, id):
#     edit_appointment = Appointment.objects.get(id = id)
#     return render(request, 'editAppointment.html', {'appointment': edit_appointment})
#
# def update_appointment(request, id):
#     update_info = Appointment.objects.get(id = id)
#     form = AppointmentForm(request.POST, instance=update_info)
#     if form.is_valid():
#         form.save()
#         return redirect('/show_appointments')
#     else:
#         return render(request, 'editAppointment.html')
#
# def delete_appointment(request, id):
#     appoint = Appointment.objects.get(id = id)
#     appoint.delete()
#     return redirect('/show_appointments')

def booking_delete(request, id):
    single_booking = Bookings.objects.get(id=id)
    single_booking.delete()
    return redirect('/dashboard')
