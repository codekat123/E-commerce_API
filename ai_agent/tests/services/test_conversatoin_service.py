from django.contrib.auth import get_user_model
from django.test import TestCase

from ai_agent.models.message import MessageRole
from ai_agent.service.conversation_service import ConversationService

User = get_user_model()


class ConversationServiceTests(TestCase):
    def setUp(self) -> None:
        self.service = ConversationService()

        self.user = User.objects.create_user(
            email="john@example.com",
            password="password123",
        )

        self.other_user = User.objects.create_user(
            email="jane@example.com",
            password="password123",
        )

    def test_create_conversation(self) -> None:
        conversation = self.service.create_conversation(
            user=self.user,
        )

        self.assertEqual(conversation.user, self.user)

    def test_get_conversation(self) -> None:
        conversation = self.service.create_conversation(
            user=self.user,
        )

        retrieved = self.service.get_conversation(
            user=self.user,
            conversation_id=conversation.id,
        )

        self.assertEqual(retrieved, conversation)

    def test_get_conversation_denies_other_users(self) -> None:
        conversation = self.service.create_conversation(
            user=self.user,
        )

        with self.assertRaises(conversation.__class__.DoesNotExist):
            self.service.get_conversation(
                user=self.other_user,
                conversation_id=conversation.id,
            )

    def test_add_user_message(self) -> None:
        conversation = self.service.create_conversation(
            user=self.user,
        )

        message = self.service.add_user_message(
            conversation=conversation,
            content="Hello",
        )

        self.assertEqual(message.conversation, conversation)
        self.assertEqual(message.role, MessageRole.USER)
        self.assertEqual(message.content, "Hello")

    def test_add_assistant_message(self) -> None:
        conversation = self.service.create_conversation(
            user=self.user,
        )

        message = self.service.add_assistant_message(
            conversation=conversation,
            content="Hi there!",
        )

        self.assertEqual(message.conversation, conversation)
        self.assertEqual(message.role, MessageRole.ASSISTANT)
        self.assertEqual(message.content, "Hi there!")
