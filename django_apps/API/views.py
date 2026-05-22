# API/views.py
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status  # Crucial for professional responses
from products.models import products
from .serializers import productserializer

@api_view(['GET'])
def get_data(request):
    product_list = products.objects.all()
    serializer = productserializer(product_list, many=True)
    # Success is assumed (HTTP 200)
    return Response(serializer.data)

@api_view(['POST'])
def add_items(request):
    # Determine if we are receiving one item or a list of items
    is_many = isinstance(request.data, list)
    
    serializer = productserializer(data=request.data, many=is_many)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)