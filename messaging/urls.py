from django.urls import path
from .views import SendMessageView, UserMessagesView, AdminMessagesView, ReplyMessageView, submit_feedback

urlpatterns = [
    path("send-message/", SendMessageView.as_view(), name="send-message"),
    path("user-messages/", UserMessagesView.as_view(), name="user-messages"),
    path("admin-messages/", AdminMessagesView.as_view(), name="admin-messages"),
    path("reply-message/<int:message_id>/", ReplyMessageView.as_view(), name="reply-message"),
    path('submit-feedback/', submit_feedback, name='submit_feedback'),
]
