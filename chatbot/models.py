from django.db import models
from django.contrib.auth.models import User

class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Session {self.user.username} - {self.title or 'No Title'}"

class Message(models.Model):
    session = models.ForeignKey(ChatSession, related_name='messages', on_delete=models.CASCADE)
    prompt = models.TextField()  # User's input
    response = models.TextField(blank=True, null=True)  # AI's response
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session {self.session.id}: {self.prompt[:30]} → {self.response[:30]}"
