from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import *
from app.serializers import *


# Create your views here.

class RegistrationAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request):
        serializer = MyUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.create(user=user)
        return Response({
            'data': {
                "user_token": token.key
            }
        }, status=status.HTTP_201_CREATED)


class AuthenticationAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request):
        serializer = AuthenticationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = MyUser.objects.filter(email=serializer.data['email']).first()
        print(228)
        if user and user.check_password(serializer.data['password']):
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'data': {
                    "user_token": token.key
                }
            }, status=status.HTTP_200_OK)
        else:
            raise AuthenticationFailed()


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        request.user.auth_token.delete()
        return Response({
            'data': {
                'message': 'logout'
            }
        })


class ProductAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request: Request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response({
            'data': serializer.data
        })

    def post(self, request: Request):
        if request.user.is_anonymous:
            raise PermissionDenied('anonymous')
        if not request.user.is_staff:
            raise PermissionDenied()

        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'data': {
                'id': serializer.data['id'],
                "message": "Product added"
            }
        })

    def delete(self, request: Request, pk):
        if request.user.is_anonymous:
            raise PermissionDenied('anonymous')
        if not request.user.is_staff:
            raise PermissionDenied()

        product = get_object_or_404(Product, pk=pk)

        product.delete()

        return Response({
            'data': {
                "message": "Product removed"
            }
        })

    def patch(self, request: Request, pk):
        if request.user.is_anonymous:
            raise PermissionDenied('anonymous')
        if not request.user.is_staff:
            raise PermissionDenied()

        product = get_object_or_404(Product, pk=pk)

        serializer = ProductSerializer(product, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response({
            'data': serializer.data
        })


class CartAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request, pk):
        if request.user.is_anonymous:
            raise PermissionDenied('anonymous')
        if request.user.is_staff:
            raise PermissionDenied()

        product = get_object_or_404(Product, pk=pk)

        cart, _ = Cart.objects.get_or_create(user=request.user)

        cart.products.add(product)

        return Response({
            'data': {
                "message": "Product add to card"
            }
        }, status=201)

    def get(self, request: Request):
        if request.user.is_anonymous:
            raise PermissionDenied('anonymous')
        if request.user.is_staff:
            raise PermissionDenied()

        cart, _ = Cart.objects.get_or_create(user=request.user)

        serializer = ProductSerializer(cart.products, many=True)

        return Response({
            'data': serializer.data
        })

    def delete(self, request: Request, pk):
        if request.user.is_anonymous:
            raise PermissionDenied('anonymous')
        if request.user.is_staff:
            raise PermissionDenied()

        cart = Cart.objects.get(user=request.user)

        product = get_object_or_404(Product, pk=pk)

        cart.products.remove(product)

        return Response({
            'data': {
                "message": "Item removed from cart"
            }
        })


class OrderAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request):
        if request.user.is_anonymous:
            raise PermissionDenied('anonymous')
        if request.user.is_staff:
            raise PermissionDenied()

        order = Order.objects.create(user=request.user)
        cart = Cart.objects.get(user=request.user)
        total = 0
        if len(cart.products.all()) == 0:
            return Response({'data': 'cart is empty'})
        for product in cart.products.all():
            order.products.add(product)
            total += product.price
        order.order_price = total

        order.save()

        return Response({
            'data': {
                "order_id": order.pk,
                "message": "Order is processed"

            }
        }, status=201)

    def get(self, request: Request):
        if request.user.is_anonymous:
            raise PermissionDenied('anonymous')
        if request.user.is_staff:
            raise PermissionDenied()

        order = Order.objects.filter(user=request.user)

        serializer = OrderSerializer(order, many=True)

        return Response({
            'data': serializer.data
        })
