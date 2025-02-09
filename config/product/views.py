from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .models import Product, Store, Review
from .serializers import ProductSerializer, StoreSerializer, ReviewSerializer

from rest_framework_simplejwt.authentication import JWTAuthentication

# ViewSet for Product
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

# Generic views for Store
class Store_View(generics.ListCreateAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class Store_Details(generics.RetrieveUpdateDestroyAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

# Generic views for Review with Token Authentication
class ReviewList(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    authentication_classes = [JWTAuthentication]  #  Authentication added
    permission_classes = [IsAuthenticated]  # Ensures only authenticated users can access

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    authentication_classes = [TokenAuthentication]  # Token Authentication added
    permission_classes = [IsAuthenticated]  # Ensures only authenticated users can access
