from rest_framework import serializers
from .models import Product
from django.contrib.auth.models import User

class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', )

class productSerializer(serializers.ModelSerializer):
    #author = userSerializer(many=False, read_only=True)
    name = serializers.CharField(source='title')
    price = serializers.FloatField(source='product_price')
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'category', ]