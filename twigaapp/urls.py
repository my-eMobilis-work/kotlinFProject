from django.contrib import admin
from django.urls import path
from twigaapp import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.index, name='index'),
    path('menu/', views.menu, name='menu'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('about/', views.about, name='about'),

    path('services/', views.services, name='services'),


    path('dashboard/', views.dashboard, name='dashboard'),
    path('users/', views.users, name='users'),
    path('user_delete/<int:id>', views.user_delete),
    path('contact/', views.contact, name='contact'),
    path('contact_delete/<int:id>', views.delete_contact),
    path('bookings/', views.bookings, name='bookings'),
    path('booking_delete/<int:id>', views.booking_delete),
    path('managers/', views.managers, name='managers'),
    path('manager_update/<int:id>', views.manager_update),
    path('manager_delete/<int:id>', views.manager_delete),
    path('manager_login/', views.manager_login, name='manager_login'),
    path('manager_register/', views.manager_register, name='manager_register'),
    path('mgr_edit_image/<int:manager_id>/', views.mgr_edit_image, name='mgr_edit_image'),
    path('mgr_delete_image/<int:manager_id>/', views.mgr_delete_image, name='mgr_delete_image'),
    path('documentation/', views.documentation, name='documentation'),
    path('manager_logout/', views.manager_logout, name='manager_logout'),

    path('gallery/', views.gallery, name='gallery'),
    path('image_delete/<int:id>', views.image_delete),
    path('upload_image/', views.upload_image, name='upload_image'),



    path('stk/', views.stk, name='stk'),
    path('token/', views.token, name='token'),

]
