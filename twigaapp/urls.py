from django.contrib import admin
from django.urls import path
from twigaapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('login/', views.login, name='login'),
    # path('index/', views.register, name='register'),

    path('', views.index, name='index'),
    path('menu/', views.menu, name='menu'),
    path('test/', views.test, name='test'),
    path('about/', views.about, name='about'),
    path('gallery/', views.gallery, name='gallery'),
    path('contact/', views.contact, name='contact'),
    path('services/', views.services, name='services'),
    path('bookings/', views.bookings, name='bookings'),


    path('dashboard/', views.dashboard, name='dashboard'),

    # path('image_delete/<int:id>', views.image_delete),
    path('upload_image/', views.upload_image, name='upload_image'),


    path('pay/', views.pay, name='pay'),
    path('stk/', views.stk, name='stk'),
    path('token/', views.token, name='token'),

]
