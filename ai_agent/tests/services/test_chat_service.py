from __future__ import annotations

from unittest.mock import create_autospec

from django.contrib.auth import get_user_model
from django.test import TestCase
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph.state import CompiledStateGraph

from ai_agent.models.conversation import Conversation
from ai_agent.models.message import MessageRole
from ai_agent.service.chat_service import ChatService
from ai_agent.service.conversation_service import ConversationService

User = get_user_model()


class ChatServiceTests(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email="john@example.com",
            password="password123",
        )

        self.other_user = User.objects.create_user(
            email="jane@example.com",
            password="password123",
        )

        self.graph = create_autospec(
            CompiledStateGraph,
            instance=True,
        )

        self.graph.invoke.return_value = {
            "messages": [
                AIMessage(
                    content="Hello from AI!",
                )
            ]
        }

        self.conversation_service = ConversationService()

        self.chat_service = ChatService(
            graph=self.graph,
            conversation_service=self.conversation_service,
        )

    def test_chat_creates_new_conversation(self) -> None:
        result = self.chat_service.chat(
            user=self.user,
            message="Hello",
        )

        self.assertIsInstance(
            result.conversation,
            Conversation,
        )

        self.assertEqual(
            result.conversation.user,
            self.user,
        )

    def test_chat_reuses_existing_conversation(self) -> None:
        conversation = self.conversation_service.create_conversation(
            user=self.user,
        )

        result = self.chat_service.chat(
            user=self.user,
            conversation_id=conversation.id,
            message="Hello",
        )

        self.assertEqual(
            result.conversation.id,
            conversation.id,
        )

    def test_chat_saves_user_and_assistant_messages(self) -> None:
        result = self.chat_service.chat(
            user=self.user,
            message="Hello",
        )

        messages = list(result.conversation.messages.order_by("created_at"))

        self.assertEqual(
            len(messages),
            2,
        )

        self.assertEqual(
            messages[0].role,
            MessageRole.USER,
        )

        self.assertEqual(
            messages[0].content,
            "Hello",
        )

        self.assertEqual(
            messages[1].role,
            MessageRole.ASSISTANT,
        )

        self.assertEqual(
            messages[1].content,
            "Hello from AI!",
        )

    def test_graph_is_invoked_once(self) -> None:
        self.chat_service.chat(
            user=self.user,
            message="Hello",
        )

        self.graph.invoke.assert_called_once()

    def test_graph_receives_human_message(self) -> None:
        self.chat_service.chat(
            user=self.user,
            message="Hello",
        )

        state = self.graph.invoke.call_args.args[0]

        messages = state["messages"]

        self.assertEqual(
            len(messages),
            1,
        )

        self.assertIsInstance(
            messages[0],
            HumanMessage,
        )

        self.assertEqual(
            messages[0].content,
            "Hello",
        )

    def test_chat_returns_ai_response(self) -> None:
        result = self.chat_service.chat(
            user=self.user,
            message="Hello",
        )

        self.assertEqual(
            result.response,
            "Hello from AI!",
        )

    def test_user_cannot_access_another_users_conversation(self) -> None:
        conversation = self.conversation_service.create_conversation(
            user=self.user,
        )

        with self.assertRaises(
            Conversation.DoesNotExist,
        ):
            self.chat_service.chat(
                user=self.other_user,
                conversation_id=conversation.id,
                message="Hello",
            )
