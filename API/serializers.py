from rest_framework import serializers
from products.models import products

class productserializer(serializers.ModelSerializer):
  class Meta:
    model = products
    fields = '__all__'