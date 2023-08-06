from rest_framework import serializers

from app.models import *


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('fio', 'password', 'email')

    def save(self, **kwargs):
        user = MyUser(
            email=self.validated_data['email'],
            username=self.validated_data['email'],
            fio=self.validated_data['fio']
        )

        user.set_password(self.validated_data['password'])
        user.save()
        return user


class AuthenticationSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
