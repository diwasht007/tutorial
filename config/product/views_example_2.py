from django.shortcuts import render
from .serializers import ProductSerializer, StoreSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Product, Store
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser


# Create your views here.
class Store_View(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    # permission_classes = [IsAdminUser]

    def get(self, request):
        store = Store.objects.all()
        serializer = StoreSerializer(store, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        serializer = StoreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Store_Details(APIView):
    def get(self, request, pk):
        try:
            store = Store.objects.get(pk=pk)
        except Store.DoesNotExist:
            return Response(
                {"Error": "Store not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = StoreSerializer(store, context={"request": request})
        return Response(serializer.data)

    def post(self, request, pk):
        store = Store.objects.get(pk=pk)
        serializer = StoreSerializer(store, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        store = Store.objects.get(pk=pk)
        store.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
def product_list_view(request):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdminUser]

    if request.method == "GET":
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(["GET", "PUT", "DELETE"])
def product_detail_view(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(
            {"Error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
        )

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
