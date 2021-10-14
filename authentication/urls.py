from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register' ),
    path('login/', views.login_user, name='login' ),
    path('logout/', views.logout_user, name='logout' ),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate_user, name='activate'),
]