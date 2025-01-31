#landing page vieW
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import LandingPage, LandingPageLink
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from .serializers import LandingPageSerializer, LandingPageLinkSerializer
from rest_framework.response import Response
from rest_framework import status
from products.serializers import  ProductSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import LandingPageSerializer

@csrf_exempt
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_or_update_landing_page(request):
    if request.method == "POST":
        # Check if the user already has a landing page
        try:
            landing_page = LandingPage.objects.get(user=request.user)
            # If found, update the landing page
            serializer = LandingPageSerializer(landing_page, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(
                    {"message": "Landing page updated", "id": landing_page.id}, 
                    status=200
                )
            return JsonResponse({"error": serializer.errors}, status=400)
        except LandingPage.DoesNotExist:
            # If no landing page exists, create a new one
            serializer = LandingPageSerializer(data=request.data)
            if serializer.is_valid():
                landing_page = serializer.save(user=request.user)  # Associate with the current user
                return JsonResponse(
                    {"message": "Landing page created", "id": landing_page.id}, 
                    status=201
                )
            return JsonResponse({"error": serializer.errors}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)


class LandingPageDetailView(APIView):
    def get(self, request, pk):
        try:
            landing_page = LandingPage.objects.get(pk=pk)
            products = landing_page.products.all()
            landing_page_data = LandingPageSerializer(landing_page).data
            products_data = ProductSerializer(products, many=True).data
            return Response({
                "landing_page": landing_page_data,
                "products": products_data
            }, status=status.HTTP_200_OK)
        except LandingPage.DoesNotExist:
            return Response({"error": "Landing page not found."}, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_landing_page(request, pk):
    try:
        landing_page = get_object_or_404(LandingPage, pk=pk)
        landing_page.delete()
        return JsonResponse({"message": "Landing page deleted"}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
# views.py

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def store_landing_page_id(request):
    try:
        # Extract request data
        pageEmail = request.data.get('email')
        landing_page_id = request.data.get('id')

        # Validate required fields
        if not pageEmail or not landing_page_id:
            return Response(
                {"error": "Email and landing_page_id are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Ensure email format and ID are valid (optional, depending on needs)
        if not isinstance(landing_page_id, int):
            return Response(
                {"error": "Invalid landing_page_id. Must be an integer."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Use get_or_create to handle duplicates
        landing_page_link, created = LandingPageLink.objects.get_or_create(
            email=pageEmail,
            defaults={"landing_page_id": landing_page_id}
        )

        if not created:
            # Update the existing landing_page_id if the record exists
            landing_page_link.landing_page_id = landing_page_id
            landing_page_link.save()

        return Response(
            {"message": "Landing page ID stored successfully!"},
            status=status.HTTP_201_CREATED
        )
    except Exception as e:
        return Response({"error": f"Internal server error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_landing_page_id_by_email(request):
    try:
        email = request.query_params.get('email')  # Get the email from query params
        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the landing page ID based on the provided email
        try:
            landing_page_link = LandingPageLink.objects.get(email=email)
            return Response({"landing_page_id": landing_page_link.landing_page_id}, status=status.HTTP_200_OK)
        except LandingPageLink.DoesNotExist:
            return Response({"error": "No landing page found for this email."}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)