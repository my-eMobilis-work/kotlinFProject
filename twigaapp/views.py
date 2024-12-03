import json
import requests
from decouple import config
from django.http import HttpResponse
from requests.auth import HTTPBasicAuth
from django.shortcuts import render, redirect
from twigaapp.models import Appointment, ImageModel, User
from twigaapp.forms import AppointmentForm, ImageUploadForm
from twigaapp.credentials import MpesaAccessToken, LipanaMpesaPassword

def register(request):
    if request.method == 'POST':
        new_user = User(
            username=request.POST['username'],
            password=request.POST['password'],
        )
        new_user.save()
        return redirect('/login')
    else:
        return render(request, 'register.html')

def login(request):
    return render(request, 'login.html')

# def index(request):
#     if request.method == 'POST':
#         if User.objects.filter(
#             username=request.POST['username'],
#             password=request.POST['password'],
#         ).exists():
#             return render(request, 'index.html')
#         else:
#             return render(request, 'login.html')
#     else:
#         return render(request, 'login.html')

def index(request):
    return render(request, 'index.html')

# TODO this uses the full page animation with 4 sliders from TULEN we saw?
#  Or keep the default
def services(request):
    return render(request, 'services.html')

def bookings(request):
    return render(request, 'bookings.html')

def menu(request):
    return render(request, 'menu.html')

def test(request):
    return render(request, 'test.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

# TODO idea from TULEN
def gallery(request):
    return render(request, 'gallery.html')

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/gallery')
    else:
        form = ImageUploadForm()
    return render(request, 'upload_image.html', {'form': form})

def show_images(request):
    images = ImageModel.objects.all()
    return render(request, 'gallery.html', {'images': images})

def image_delete(request, id):
    image = ImageModel.objects.get(id=id)
    image.delete()
    return redirect('/gallery')



def token(request):
    consumer_key = config('CONSUMER_KEY')
    consumer_secret = config('CONSUMER_SECRET')
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]
    return render(request, 'token.html', {"token":validated_mpesa_access_token})

def pay(request):
   return render(request, 'pay.html')

def stk(request):
    if request.method =="POST":
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


# TODO idea from NickelFox(Can't it uses react but we can copy its design and implement in bootstrap)
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')