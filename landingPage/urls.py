from django.urls import path
from .views import create_or_update_landing_page, delete_landing_page,store_landing_page_id, LandingPageDetailView, get_landing_page_id_by_email

urlpatterns = [
    path("create/", create_or_update_landing_page, name="create_landing_page"),
    path("<int:pk>/", LandingPageDetailView.as_view(), name="get_landing_page"),
    path("<int:pk>/update/", create_or_update_landing_page, name="update_landing_page"),
    path("<int:pk>/delete/", delete_landing_page, name="delete_landing_page"),
    path('store-landing-page-id/', store_landing_page_id, name='store_landing_page_id'),
    path('get-landing-page-id/', get_landing_page_id_by_email, name='get_landing_page_id_by_email'),
]
