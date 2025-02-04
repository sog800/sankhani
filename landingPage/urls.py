from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_or_update_landing_page, name="create_landing_page"),
    path("<int:pk>/", views.LandingPageDetailView.as_view(), name="get_landing_page"),
    path("<int:pk>/update/", views.create_or_update_landing_page, name="update_landing_page"),
    path("<int:pk>/delete/", views.delete_landing_page, name="delete_landing_page"),
    path('store-landing-page-id/', views.store_landing_page_id, name='store_landing_page_id'),
    path('get-landing-page-id/', views.get_landing_page_id_by_email, name='get_landing_page_id_by_email'),
    path("feedback/", views.ListFeedbackView.as_view(), name="list-feedback"),
    path("feedback/create/", views.CreateFeedbackView.as_view(), name="create-feedback"),
    path("feedback/delete/<int:pk>/", views.DeleteFeedbackView.as_view(), name="delete-feedback"),
]
