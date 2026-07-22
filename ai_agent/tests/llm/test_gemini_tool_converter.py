from django.test import TestCase
from google.genai import types

from ai_agent.llm.tool_converter import GeminiToolConverter
from ai_agent.tools.schema import (
    ToolDefinition,
    ToolParameter,
    ToolParameterType,
)


class GeminiToolConverterTests(TestCase):
    def setUp(self) -> None:
        self.converter = GeminiToolConverter()

    def test_converts_single_definition(self) -> None:
        definition = ToolDefinition(
            name="get_weather",
            description="Get the current weather.",
            parameters=[],
        )

        declaration = self.converter.convert(definition)

        self.assertEqual(declaration.name, "get_weather")
        self.assertEqual(
            declaration.description,
            "Get the current weather.",
        )
        self.assertEqual(
            declaration.parameters.type,
            types.Type.OBJECT,
        )
        self.assertEqual(
            declaration.parameters.properties,
            {},
        )
        self.assertEqual(
            declaration.parameters.required,
            [],
        )

    def test_converts_multiple_definitions(self) -> None:
        definitions = [
            ToolDefinition(
                name="tool_one",
                description="First tool.",
                parameters=[],
            ),
            ToolDefinition(
                name="tool_two",
                description="Second tool.",
                parameters=[],
            ),
        ]

        declarations = self.converter.convert_many(definitions)

        self.assertEqual(len(declarations), 2)

        self.assertEqual(
            declarations[0].name,
            "tool_one",
        )
        self.assertEqual(
            declarations[1].name,
            "tool_two",
        )

    def test_marks_required_parameters(self) -> None:
        definition = ToolDefinition(
            name="get_weather",
            description="",
            parameters=[
                ToolParameter(
                    name="city",
                    type=ToolParameterType.STRING,
                    description="City name.",
                    required=True,
                ),
            ],
        )

        declaration = self.converter.convert(definition)

        schema = declaration.parameters

        self.assertEqual(
            schema.required,
            ["city"],
        )

        self.assertIn(
            "city",
            schema.properties,
        )

    def test_omits_optional_parameters_from_required(self) -> None:
        definition = ToolDefinition(
            name="get_weather",
            description="",
            parameters=[
                ToolParameter(
                    name="city",
                    type=ToolParameterType.STRING,
                    description="City name.",
                    required=False,
                ),
            ],
        )

        declaration = self.converter.convert(definition)

        self.assertEqual(
            declaration.parameters.required,
            [],
        )

    def test_converts_all_parameter_types(self) -> None:
        definition = ToolDefinition(
            name="tool",
            description="",
            parameters=[
                ToolParameter(
                    name="string",
                    type=ToolParameterType.STRING,
                    description="",
                    required=True,
                ),
                ToolParameter(
                    name="integer",
                    type=ToolParameterType.INTEGER,
                    description="",
                    required=True,
                ),
                ToolParameter(
                    name="number",
                    type=ToolParameterType.NUMBER,
                    description="",
                    required=True,
                ),
                ToolParameter(
                    name="boolean",
                    type=ToolParameterType.BOOLEAN,
                    description="",
                    required=True,
                ),
                ToolParameter(
                    name="array",
                    type=ToolParameterType.ARRAY,
                    description="",
                    required=True,
                ),
                ToolParameter(
                    name="object",
                    type=ToolParameterType.OBJECT,
                    description="",
                    required=True,
                ),
            ],
        )

        declaration = self.converter.convert(definition)

        properties = declaration.parameters.properties

        self.assertEqual(
            properties["string"].type,
            types.Type.STRING,
        )
        self.assertEqual(
            properties["integer"].type,
            types.Type.INTEGER,
        )
        self.assertEqual(
            properties["number"].type,
            types.Type.NUMBER,
        )
        self.assertEqual(
            properties["boolean"].type,
            types.Type.BOOLEAN,
        )
        self.assertEqual(
            properties["array"].type,
            types.Type.ARRAY,
        )
        self.assertEqual(
            properties["object"].type,
            types.Type.OBJECT,
        )
