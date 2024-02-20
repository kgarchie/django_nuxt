from django.urls import path, include
from . import views

app_name = 'api'

urlpatterns = [
    path('customers/', views.CustomerView.as_view()),
    path('products', views.ProductView.as_view()),
    path('orders', views.OrderView.as_view()),
    path('auth/login', views.LoginView.as_view()),
    path('auth/logout', views.LogoutView.as_view()),
    path('auth/signup', views.SignupView.as_view()),
    path('auth/refresh', views.RefreshView.as_view()),
]