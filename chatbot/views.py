
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authentication import SessionAuthentication,BasicAuthentication
from google.generativeai import configure, GenerativeModel
from .models import ChatSession, Message
from rest_framework_simplejwt.authentication import  JWTAuthentication
from .serializers import RegisterSerializer, UserSerializer, ChatSessionSerializer, MessageSerializer
from rest_framework.parsers import MultiPartParser, FormParser , JSONParser


configure(api_key="")
gemini_model = GenerativeModel("gemini-2.0-flash")

class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class LoginAPIView(generics.GenericAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.get()
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class ChatSessionListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ChatSessionSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication,SessionAuthentication,BasicAuthentication]
    parser_classes = [MultiPartParser,FormParser]
    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ChatSessionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChatSessionSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication,SessionAuthentication,BasicAuthentication]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user)


class MessageListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication,SessionAuthentication,BasicAuthentication]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    def get(self, request, session_pk):
        """Retrieve all messages for a specific chat session"""
        try:
            session = ChatSession.objects.get(id=session_pk, user=request.user)
        except ChatSession.DoesNotExist:
            return Response({"error": "Chat session not found"}, status=status.HTTP_404_NOT_FOUND)

        messages = Message.objects.filter(session=session)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request, session_pk):
        try:
            session = ChatSession.objects.get(id=session_pk, user=request.user)
        except ChatSession.DoesNotExist:
            return Response({"error": "Chat session not found"}, status=status.HTTP_404_NOT_FOUND)

        user_prompt = request.data.get("prompt", "").strip()
        if not user_prompt:
            return Response({"error": "Prompt cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)

        response = gemini_model.generate_content(user_prompt)
        bot_reply = response.text if response else "Sorry, I couldn't generate a response."

        message = Message.objects.create(session=session, prompt=user_prompt, response=bot_reply)

        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)

