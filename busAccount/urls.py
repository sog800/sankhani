from django.urls import path
from .views import RegisterView, LogoutView, SubscriberCreateAPIView
from .views import  get_profile, edit_profile, LoginView, RefreshAccessTokenView, DeleteAccountView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('get-profile/', get_profile, name='user_business_profile'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('accounts/delete/', DeleteAccountView.as_view(), name='delete_account'),
    path('subscribe/', SubscriberCreateAPIView.as_view(), name='subscriber-create'),


    # toke handling  login and logout
    path('login/', LoginView.as_view(), name='token_obtain_pair'),  # Login
    path('token/refresh-access/', RefreshAccessTokenView.as_view(), name='refresh_access_token'),
    path('logout/', LogoutView.as_view(), name='logout'),  # Logout

]
