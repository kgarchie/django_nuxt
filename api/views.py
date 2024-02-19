from .serializers import CustomerSerializer, ProductSerializer, OrderSerializer
from .models import Customer, Product, Order
from rest_framework.views import APIView
from rest_framework.response import Response


class CustomerView(APIView):
    def get(self, request, pk=None):
        if pk:
            customer = Customer.objects.get(pk=pk)
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    def post(self, request):
        customer = request.data
        serializer = CustomerSerializer(data=customer)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        
    def put(self, request, pk):
        saved_customer = Customer.objects.get(pk=pk)
        data = request.data
        serializer = CustomerSerializer(instance=saved_customer, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        
    def delete(self, request, pk):
        customer = Customer.objects.get(pk=pk)
        customer.delete()
        return Response("Customer deleted", status=204)
    

class ProductView(APIView):
    def get(self, request, pk=None):
        if pk:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        product = request.data
        serializer = ProductSerializer(data=product)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        
    def put(self, request, pk):
        saved_product = Product.objects.get(pk=pk)
        data = request.data
        serializer = ProductSerializer(instance=saved_product, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        
    def delete(self, request, pk):
        product = Product.objects.get(pk=pk)
        product.delete()
        return Response("Product deleted", status=204)


class OrderView(APIView):
    def get(self, request, pk=None):
        if pk:
            order = Order.objects.get(pk=pk)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        order = request.data
        serializer = OrderSerializer(data=order)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        
    def put(self, request, pk):
        saved_order = Order.objects.get(pk=pk)
        data = request.data
        serializer = OrderSerializer(instance=saved_order, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        
    def delete(self, request, pk):
        order = Order.objects.get(pk=pk)
        order.delete()
        return Response("Order deleted", status=204)
