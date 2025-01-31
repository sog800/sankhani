from django.urls import path
from .views import RegisterView, LogoutView
from .views import  get_profile, edit_profile, LoginView, RefreshAccessTokenView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('get-profile/', get_profile, name='user_business_profile'),
    path('edit-profile/', edit_profile, name='edit_profile'),

    # toke handling  login and logout
    path('login/', LoginView.as_view(), name='token_obtain_pair'),  # Login
    path('token/refresh-access/', RefreshAccessTokenView.as_view(), name='refresh_access_token'),
    path('logout/', LogoutView.as_view(), name='logout'),  # Logout
]
