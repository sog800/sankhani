from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.SearchProductView.as_view(), name='search-products'),
    path('product-ratings/', views.ProductRatingView.as_view(), name='product-rating'),
    # /products/ handles listing and creating products.
    path("create/", views.ProductCreateView.as_view(), name="product-create"),
    # /products/<id>/ handles retrieving, updating, and deleting specific
    path("<int:pk>/", views.ProductDetailView.as_view(), name="product-detail"),
    path("filter/", views.ProductFilteredView.as_view(), name="product-filter"),
    path('user-products/', views.UserProductListView.as_view(), name='user-product-list'),
    path("keep-alive/", views.keep_alive, name="keep_alive"),
    path('list-all/', views.ProductListView.as_view(), name='list-products'),
]
