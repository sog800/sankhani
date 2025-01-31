from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from .models import UserBusinessProfile
from .serializers import UserBusinessProfileSerializer, RegisterSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from datetime import timedelta
from django.utils.timezone import now
from django.contrib.auth import authenticate
from .models import Token
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_500_INTERNAL_SERVER_ERROR
from products.models import Product, LandingPage
from busAccount.models import Feedback

# Business profile views

@csrf_exempt
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_profile(request):
    try:
        # Get the profile of the authenticated user
        profile = UserBusinessProfile.objects.get(user=request.user)

        # Serialize the profile data
        serializer = UserBusinessProfileSerializer(profile)
        
        return JsonResponse(serializer.data, status=200)
    except UserBusinessProfile.DoesNotExist:
        return JsonResponse({"error": "Profile not found."}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    

@csrf_exempt
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_profile(request):
    # Get the current user's profile
    try:
        profile = UserBusinessProfile.objects.get(user=request.user)  # Find the profile for the current user
    except UserBusinessProfile.DoesNotExist:
        return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

    # Serialize the incoming data with the profile
    serializer = UserBusinessProfileSerializer(profile, data=request.data, partial=True)  # Allow partial updates

    if serializer.is_valid():
        # Save the updated profile
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUES)
        

# token handling view and login and log out and register

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import get_user_model  # Import the custom user model dynamically
from .serializers import RegisterSerializer

User = get_user_model()  # Get the custom user model

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer

User = get_user_model()  # Get the custom user model

class RegisterView(APIView):
    def post(self, request):
        email = request.data.get("email")
        username = request.data.get("username")  # Renamed 'user' to 'username' for clarity

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "This username is already in use. Please choose another one or add a number."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "This email is already in use. Please use a different email."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User created successfully!"},
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def post(self, request):
        # Get the user from the request
        user = request.user

        # Delete all tokens for the user
        Token.objects.filter(user=user).delete()

        return Response({"message": "Logged out successfully"}, status=200)

@method_decorator(csrf_exempt, name='dispatch')
class RefreshAccessTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Get the expired access token from the request
        expired_access_token = request.data.get("expired_access_token")
        try:
            # Retrieve the token entry from the database
            token_entry = Token.objects.get(access_token=expired_access_token)

            # Check if the refresh token has expired
            if token_entry.is_refresh_expired():
                return Response({"error": "Refresh token expired"}, status=401)
                
            # Generate a new access token
            refresh = RefreshToken(token_entry.refresh_token)
            new_access = refresh.access_token

            # Update the access token in the database
            token_entry.access_token = str(new_access)
            token_entry.access_expires_at = now() + timedelta(minutes=5)
            token_entry.save()
            
            # Return the new access token
            return Response({"access": str(new_access)}, status=200)

        except Token.DoesNotExist:
            print(f"Invalid access token: {expired_access_token}")
            return Response({"error": "Invalid access token"}, status=401)
        except Exception as e:
            print(f"Unexpected error: {e}")
            return Response({"error": "Server error"}, status=500)

# log in

class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        # Validate input
        if not username or not password:
            return Response({"error": "Username and password are required."}, status=HTTP_400_BAD_REQUEST)

        # Authenticate the user
        user = authenticate(username=username, password=password)
        if not user:
            return Response({"error": "Invalid credentials."}, status=HTTP_401_UNAUTHORIZED)

        try:
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token

            # Save tokens in the database
            Token.objects.create(
                user=user,
                access_token=str(access),
                refresh_token=str(refresh),
                access_expires_at=now() + timedelta(minutes=15),  # Access token expires in 15 minutes
                refresh_expires_at=now() + timedelta(days=7),  # Refresh token expires in 7 days
            )

            return Response({"access": str(access)}, status=200)

        except Exception as e:
            return Response({"error": "Something went wrong on the server. Please try again later."}, status=HTTP_500_INTERNAL_SERVER_ERROR)

class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def delete(self, request, *args, **kwargs):
        user = request.user
        feedback = request.data.get('feedback', '')

        # Store the feedback in the Feedback model (before deleting the user and data)
        if feedback:
            Feedback.objects.create(user=user, feedback=feedback)

        # Delete the user's associated posts, landing pages, etc.
        Product.objects.filter(user=user).delete()
        LandingPage.objects.filter(user=user).delete()

        # Finally, delete the user account
        user.delete()

        return JsonResponse({'message': 'Account and associated data deleted successfully'}, status=200)
