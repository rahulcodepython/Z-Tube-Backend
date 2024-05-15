from django.urls import path
from . import views

urlpatterns = [
    path("create-product/", views.CreateProductView.as_view()),
    path("get-all-my-products/", views.GetAllMyProductsView.as_view()),
]
