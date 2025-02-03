from rest_framework import generics, permissions,status, permissions
from .models import Product,ProductRating
from .serializers import ProductSerializer
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework.permissions import IsAuthenticated
from .utils.imageCompresor import optimize_image
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics, permissions
from .models import Product
from .serializers import ProductSerializer


class ProductCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Get the current user details
        user = self.request.user

        # Check if an image was uploaded with the request
        product_picture = self.request.FILES.get('product_picture')
        if product_picture:
            # Optimize the image before saving
            optimized_image = optimize_image(product_picture)
            serializer.save(
                user=user, 
                email=user.email, 
                product_picture=optimized_image
            )
        else:
            serializer.save(user=user, email=user.email)



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
    pagination_class = ProductPagination
    product_fields = {field.name for field in Product._meta.get_fields()}  # Cached for efficiency

    def get(self, request):
        filters = {}

        for key, value in request.query_params.items():
            if key in self.product_fields:
                filters[f"{key}__iexact"] = value  # Case-insensitive filtering

        products = Product.objects.filter(**filters).order_by("-id")

        paginator = self.pagination_class()
        paginated_products = paginator.paginate_queryset(products, request, view=self)

        if paginated_products is not None:
            serializer = ProductSerializer(paginated_products, many=True)
            return paginator.get_paginated_response(serializer.data)

        return Response({"detail": "No matching products found."}, status=status.HTTP_404_NOT_FOUND)


class ProductListView(APIView):
    pagination_class = ProductPagination

    def get(self, request):
        products = Product.objects.all()  # Fetch all products
        paginator = self.pagination_class()
        paginated_products = paginator.paginate_queryset(products, request)
        
        # Ensure pagination works correctly
        if paginated_products is not None:
            serializer = ProductSerializer(paginated_products, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        # In case of no pagination
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    

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



from django.http import JsonResponse

def keep_alive(request):
    return JsonResponse({"status": "alive"})
