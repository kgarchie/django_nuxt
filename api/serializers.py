from rest_framework import serializers
from .models import Customer, Product, Order

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['uuid', 'username', 'email', 'phone']
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        
class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = Order
        fields = '__all__'