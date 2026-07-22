from django.test import TestCase

from ai_agent.tests.tools.fakes.fake_tool import FakeTool
from ai_agent.tools.registry import ToolRegistry


class ToolRegistryTests(TestCase):
    def setUp(self) -> None:
        self.tool = FakeTool()
        self.registry = ToolRegistry(
            tools=[self.tool],
        )

    def test_get_returns_registered_tool(self) -> None:
        tool = self.registry.get("fake_tool")

        self.assertIs(tool, self.tool)

    def test_get_returns_none_for_unknown_tool(self) -> None:
        tool = self.registry.get("unknown_tool")

        self.assertIsNone(tool)

    def test_list_definitions_returns_registered_tool_definitions(self) -> None:
        definitions = self.registry.definitions()

        self.assertEqual(len(definitions), 1)
        self.assertEqual(definitions[0].name, "fake_tool")
        self.assertEqual(
            definitions[0].description,
            "Fake tool used for tests.",
        )
