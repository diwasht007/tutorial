from django.shortcuts import render
from .serializers import ProductSerializer,StoreSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Product
from rest_framework import status

#function based view creation


@api_view(["GET", "POST"])
def product_list_view(request):
    if request.method == "GET":
        products = Product.objects.all()
        serializer = StoreSerializer(products, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = StoreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(["GET", "PUT", "DELETE"])
def product_detail_view(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({'Error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    elif request.method == "PUT":
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
