from rest_framework import generics, permissions,status, permissions
from .models import Product,ProductRating
from .serializers import ProductSerializer, ProductRatingSerializer
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework.permissions import IsAuthenticated


#  product crude api view

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, email=self.request.user.email)


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




class ProductFilteredView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        # Retrieve query parameters
        district = request.query_params.get("district")
        category = request.query_params.get("category")

        # Build filters dynamically
        filters = {}
        if district:
            filters["district__iexact"] = district  # Case-insensitive filter
        if category:
            filters["category__iexact"] = category  # Case-insensitive filter

        # Fetch products with or without filters
        products = Product.objects.filter(**filters)

        # Return response
        if products.exists():
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # Friendly message if no products match the filters
            message = (
                "No products found."
                if not district and not category
                else f"No products found for district '{district}' and category '{category}'."
            )
            return Response(
                {"detail": message},
                status=status.HTTP_404_NOT_FOUND,
            )
# search engine
class SearchProductView(APIView):
    def get(self, request):
        query = request.GET.get('q', '')  # Get search query from request
        if query:
            products = Product.objects.filter(title__icontains=query)  # Use 'title' instead of 'name'
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
