from .sms import SMS
from .serializers import CustomerSerializer, ProductSerializer, OrderSerializer
from .models import Customer, Product, Order, Session
from rest_framework.views import APIView
from rest_framework.response import Response
from typing import Any, Dict


def format(statusCode: int, body: Any) -> Dict[str, Any]:
    return {"statusCode": statusCode, "body": body}


def login(user: Customer) -> str:
    session = Session.objects.create(user=user)
    return session.token


def logout(token: str | None) -> None:
    if not token:
        return
    session = Session.objects.get(token=token)
    session.valid = False
    session.save()


def authenticate(username: str, password: str) -> Customer:
    try:
        user = Customer.objects.get(username=username)
    except Customer.DoesNotExist:
        return None
    if user.check_password(password):
        return user
    return None


def get_bearer_token(request) -> str:
    header = request.headers.get("Authorization")
    if not header:
        return None
    token = header.split(" ")
    if len(token) != 2 or token[0] != "Bearer" or token[1].strip() == "":
        return None
    return token[1]


class CustomerView(APIView):
    def get(self, request, pk=None):
        if pk:
            customer = Customer.objects.get(pk=pk)
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(format(200, serializer.data))

    def post(self, request):
        customer = request.data
        serializer = CustomerSerializer(data=customer)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(format(201, serializer.data), status=201)

    def put(self, request, pk):
        saved_customer = Customer.objects.get(pk=pk)
        data = request.data
        serializer = CustomerSerializer(
            instance=saved_customer, data=data, partial=True
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(format(200, serializer.data))

    def delete(self, request, pk):
        customer = Customer.objects.get(pk=pk)
        customer.delete()
        return Response(format(204, "Customer deleted"), status=204)


class ProductView(APIView):
    def get(self, request, pk=None):
        if pk:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(format(200, serializer.data))

    def post(self, request):
        product = request.data
        serializer = ProductSerializer(data=product)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(format(201, serializer.data), status=201)

    def put(self, request, pk):
        saved_product = Product.objects.get(pk=pk)
        data = request.data
        serializer = ProductSerializer(instance=saved_product, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(format(200, serializer.data))

    def delete(self, request, pk):
        product = Product.objects.get(pk=pk)
        product.delete()
        return Response(format(204, "Product deleted"), status=204)


class OrderView(APIView):
    def get(self, request):
        bearer = get_bearer_token(request)

        if not bearer:
            return Response(format(401, "No Token"), status=401)

        customer = Session.objects.get(token=bearer).user
        orders = Order.objects.filter(customer=customer)

        serializer = OrderSerializer(orders, many=True)
        return Response(format(200, serializer.data))

    def post(self, request):
        items = request.data
        customer = get_bearer_token(request)

        if not customer:
            return Response(format(401, "No Token"), status=401)

        customer = Session.objects.get(token=customer).user

        for item in items:
            Order.objects.create(customer=customer, product_id=item["id"])

        SMS().send(customer.phone, f"Your order with id {self.id} has been placed successfully.")
        return Response(format(201, "Order placed successfully"), status=201)

    def put(self, request, pk):
        saved_order = Order.objects.get(pk=pk)
        data = request.data
        serializer = OrderSerializer(instance=saved_order, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(format(200, serializer.data))

    def delete(self, request, pk):
        order = Order.objects.get(pk=pk)
        order.delete()
        return Response(format(204, "Order deleted"), status=204)


class LoginView(APIView):
    def post(self, request):
        data = request.data
        email = data.get("email")
        password = data.get("password")
        user = authenticate(username=email, password=password)
        if user:
            token = login(user)
            return Response(format(200, token), status=200)
        return Response(format(401, "Invalid credentials"), status=401)


class LogoutView(APIView):
    def get(self, request):
        token = get_bearer_token(request)
        logout(token)
        return Response(format(200, "Logout successful"), status=200)


class SignupView(APIView):
    def post(self, request):
        data = request.data
        data["username"] = data.get("email")

        serializer = CustomerSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.instance
            user.set_password(data.get("password"))
            user.save()
            token = login(user)
            return Response(format(201, token), status=201)
        return Response(
            format(400, serializer.errors or "Unkown Serialiser Error"), status=400
        )


class RefreshView(APIView):
    def get(self, request):
        token = get_bearer_token(request)
        if not token:
            return Response(format(400, "Invalid token"), status=400)
        session = None

        try:
            session = Session.objects.get(token=token)
        except Session.DoesNotExist:
            return Response(format(400, "Invalid token"), status=400)
        
        if not session.valid:
            return Response(format(401, "Invalid token"), status=401)
        return Response(format(200, CustomerSerializer(session.user).data), status=200)
    