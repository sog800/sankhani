from django.urls import path
from . import views
from .views import keep_alive

urlpatterns = [
    path('search/', views.SearchProductView.as_view(), name='search-products'),
    path('product-ratings/', views.ProductRatingView.as_view(), name='product-rating'),
    # /products/ handles listing and creating products.
    path("create/", views.ProductCreateView.as_view(), name="product-list"),
    # /products/<id>/ handles retrieving, updating, and deleting specific
    path("<int:pk>/", views.ProductDetailView.as_view(), name="product-detail"),
    path("filter/", views.ProductFilteredView.as_view(), name="product-filter"),
    path('user-products/', views.UserProductListView.as_view(), name='user-product-list'),
    path("keep-alive/", keep_alive, name="keep_alive"),
]
