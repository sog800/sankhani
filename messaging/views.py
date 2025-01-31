from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import Message
from .serializers import MessageSerializer

class SendMessageView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        message_text = request.data.get("message")
        receiver_id = request.data.get("receiver_id")  # If sending to a specific user

        if not message_text:
            return Response({"error": "Message cannot be empty"}, status=400)

        sender = request.user
        if receiver_id:
            try:
                receiver = User.objects.get(id=receiver_id)
                Message.objects.create(sender=sender, receiver=receiver, message=message_text)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=404)
        else:
            # Send to all users
            users = User.objects.exclude(is_superuser=True)
            for user in users:
                Message.objects.create(sender=sender, receiver=user, message=message_text)

        return Response({"success": "Message sent successfully!"})

class UserMessagesView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(receiver=self.request.user).order_by('-created_at')

class AdminMessagesView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return Message.objects.all().order_by('-created_at')

class ReplyMessageView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, message_id):
        try:
            message = Message.objects.get(id=message_id, receiver=request.user)
        except Message.DoesNotExist:
            return Response({"error": "Message not found"}, status=404)

        reply_text = request.data.get("message")
        if not reply_text:
            return Response({"error": "Reply cannot be empty"}, status=400)

        Message.objects.create(sender=request.user, receiver=message.sender, message=reply_text)
        return Response({"success": "Reply sent!"})


# feed back

# views.py
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import FeedBack
from .serializers import FeedBackSerializer

@csrf_exempt
def submit_feedback(request):
    if request.method == 'POST':
        # Parse the JSON data from the frontend
        data = json.loads(request.body)
        serializer = FeedBackSerializer(data=data)
        
        if serializer.is_valid():
            # Save the feedback to the database
            serializer.save()
            return JsonResponse({"message": "Feedback submitted successfully!"}, status=200)
        else:
            return JsonResponse({"error": "Invalid data"}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)
