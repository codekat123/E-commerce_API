from django.db import models

from ai_agent.models.conversation import Conversation


class MessageRole(models.TextChoices):
    USER = "user", "User"
    ASSISTANT = "assistant", "Assistant"
    SYSTEM = "system", "System"
    TOOL = "tool", "Tool"


class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages",
    )

    role = models.CharField(
        max_length=20,
        choices=MessageRole,
    )

    content = models.TextField()

    tool_calls = models.JSONField(
        default=list,
        blank=True,
    )

    tool_call_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    tool_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["created_at"]
