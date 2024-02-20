from django.urls import path, include
from . import views

app_name = 'api'

urlpatterns = [
    path('customers/', views.CustomerView.as_view(), name='customers'),
    path('customers/<uuid:uuid>', views.CustomerView.as_view(), name='customer'),
    path('products', views.ProductView.as_view(), name='products'),
    path('orders', views.OrderView.as_view(), name='orders'),
    path('auth/login', views.LoginView.as_view(), name='login'),
    path('auth/logout', views.LogoutView.as_view(), name='logout'),
    path('auth/signup', views.SignupView.as_view(), name='signup'),
    path('auth/refresh', views.RefreshView.as_view(), name='refresh'),
]