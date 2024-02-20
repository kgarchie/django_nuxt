from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Customer, Product, Session


class CustomerViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = Customer.objects.create(username='test_customer', phone='1234567890')

    def test_get_all_customers(self):
        response = self.client.get(reverse('api:customers'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_customer(self):
        response = self.client.get(reverse('api:customer', args=[self.customer.uuid]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_customer(self):
        response = self.client.post(reverse('api:customers'), {'username': 'test_customer2', 'phone': '1234567890'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_customer_invalid(self):
        response = self.client.post(reverse('api:customers'), {'username': 'test_customer2'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ProductViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.product = Product.objects.create(name='test_product', price=100, stock=10)

    def test_get_all_products(self):
        response = self.client.get(reverse('api:products'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_product(self):
        response = self.client.post(reverse('api:products'), {'name': 'test_product2', 'price': 100, 'stock': 10})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_product_invalid(self):
        response = self.client.post(reverse('api:products'), {'name': 'test_product2'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class OrderViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = Customer.objects.create(username='test_customer', phone='1234567890')
        self.product = Product.objects.create(name='test_product', price=100, stock=10)
        self.session = Session.objects.create(user=self.customer)

    def test_get_all_orders(self):
        response = self.client.get(reverse('api:orders'), HTTP_AUTHORIZATION=f'Bearer {self.session.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_order(self):
        response = self.client.post(reverse('api:orders'), [{'id': self.product.id}], HTTP_AUTHORIZATION=f'Bearer {self.session.token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_order_forbidden(self):
        response = self.client.post(reverse('api:orders'), [{'id': self.product.id}])
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_order_invalid(self):
        response = self.client.post(reverse('api:orders'), [{'id': self.product.id}], HTTP_AUTHORIZATION=f'Bearer {self.session.token}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AuthViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = Customer.objects.create(email='test_customer', phone='1234567890')
        self.customer.set_password('test_password')
        self.customer.save()
        self.token = Session.objects.create(user=self.customer).token

    def test_login(self):
        response = self.client.post(reverse('api:login'), {'email': 'test_customer', 'password': 'test_password'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_login_invalid(self):
        response = self.client.post(reverse('api:login'), {'username': 'test_customer'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_logout(self):
        response = self.client.get(reverse('api:logout'), HTTP_AUTHORIZATION='Bearer test_token')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_signup(self):
        response = self.client.post(reverse('api:signup'), {'email': 'test_customer2', 'phone': '1234567890', 'password': 'test_password'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_signup_invalid(self):
        response = self.client.post(reverse('api:signup'), {'email': 'test_customer2', 'phone': '1234567890'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_refresh(self):
        response = self.client.get(reverse('api:refresh'), HTTP_AUTHORIZATION='Bearer ' + self.token.__str__())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_refresh_invalid(self):
        response = self.client.get(reverse('api:refresh'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
