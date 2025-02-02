from rest_framework import generics, permissions,status, permissions
from .models import Product,ProductRating
from .serializers import ProductSerializer, ProductRatingSerializer
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework.permissions import IsAuthenticated
from .utils.imageCompresor import optimize_image


#  product crude api view

from django.core.cache import cache
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics, permissions
from .models import Product
from .serializers import ProductSerializer


class ProductCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Only logged-in users can create

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)  # Assign product to the logged-in user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# product filter

class UserProductListView(generics.ListAPIView):
    """
    View to list all products for the authenticated user.
    """
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access this view
    serializer_class = ProductSerializer

    def get_queryset(self):
        """
        This view should return a list of products for the currently authenticated user.
        """
        return Product.objects.filter(user=self.request.user)



class ProductPagination(PageNumberPagination):
    page_size = 20  # Default: 20 products per page
    page_size_query_param = "page_size"  # Allow frontend to request custom page size
    max_page_size = 100  # Limit maximum page size
    
class ProductFilteredView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        filters = {}

        # Dynamic filtering based on query params
        for key, value in request.query_params.items():
            if key in [field.name for field in Product._meta.get_fields()]:
                filters[f"{key}__iexact"] = value  # Case-insensitive filtering

        # Filter products
        products = Product.objects.filter(**filters).order_by("-id")  # Newest products first

        # Apply pagination
        paginator = ProductPagination()
        paginated_products = paginator.paginate_queryset(products, request, view=self)

        if paginated_products is not None:
            serializer = ProductSerializer(paginated_products, many=True)
            return paginator.get_paginated_response(serializer.data)

        return Response({"detail": "No matching products found."}, status=status.HTTP_404_NOT_FOUND)




# search engine
from django.db.models import Q
class SearchProductView(APIView):
    def get(self, request):
        query = request.GET.get('q', '').strip()  # Get search query from request and remove extra spaces

        if query:
            # Filter products where title or category contains the query (case-insensitive)
            products = Product.objects.filter(
                Q(title__icontains=query) | Q(category__icontains=query)
            )
        else:
            products = Product.objects.all()

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# product rating

class ProductRatingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Get product and rating from request
        product = Product.objects.get(id=request.data['product'])
        rating_value = request.data['rating']

        # Check if the user has already rated the product
        existing_rating = ProductRating.objects.filter(product=product, user=request.user).first()
        if existing_rating:
            return Response({"detail": "You have already rated this product."}, status=status.HTTP_400_BAD_REQUEST)

        # Create new rating
        rating = ProductRating.objects.create(
            product=product,
            user=request.user,
            rating=rating_value
        )
        
        # Update the product's average rating
        product.update_average_rating()

        return Response({
            "detail": "Rating submitted successfully.",
            "average_rating": product.average_rating  # Send updated average rating
        }, status=status.HTTP_201_CREATED)
