from django.urls import path
from . import views 


urlpatterns = [
    path('', views.Home, name='home'),
    #path('student-dashboard/tutorials' , views.view_tutorials, name='view_tutorials'),



    path('register/', views.RegisterView, name='register'),
    path('login/', views.LoginView, name='login'),
    path('instructor-dashboard/', views.InstructorDashboard, name='instructor-dashboard'),

    path('logout/', views.LogoutView, name='logout'),
    path('forgot-password/', views.ForgotPassword, name='forgot-password'),
    path('password-reset-sent/<str:reset_id>/', views.PasswordResetSent, name='password-reset-sent'),
    path('reset-password/<str:reset_id>/', views.ResetPassword, name='reset-password'),
]