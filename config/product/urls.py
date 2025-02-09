from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("products", views.ProductViewSet, basename="product")

urlpatterns = [
    path("", include(router.urls)),
    path("store/", views.Store_View.as_view(), name="store_list"),
    path("store/<int:pk>/", views.Store_Details.as_view(), name="store_detail"),
    path("review/", views.ReviewList.as_view(), name="review_list"),
    path("review/<int:pk>/", views.ReviewDetail.as_view(), name="review_detail"),
]
