from __future__ import annotations

from collections.abc import Iterable

from google.genai import types

from ai_agent.tools.schema import ToolDefinition, ToolParameterType


class GeminiToolConverter:
    """
    Converts provider-agnostic tool definitions into
    Gemini FunctionDeclarations.
    """

    _TYPE_MAPPING = {
        ToolParameterType.STRING: types.Type.STRING,
        ToolParameterType.INTEGER: types.Type.INTEGER,
        ToolParameterType.NUMBER: types.Type.NUMBER,
        ToolParameterType.BOOLEAN: types.Type.BOOLEAN,
        ToolParameterType.ARRAY: types.Type.ARRAY,
        ToolParameterType.OBJECT: types.Type.OBJECT,
    }

    def convert(
        self,
        definition: ToolDefinition,
    ) -> types.FunctionDeclaration:
        return types.FunctionDeclaration(
            name=definition.name,
            description=definition.description,
            parameters=self._build_schema(definition),
        )

    def convert_many(
        self,
        definitions: Iterable[ToolDefinition],
    ) -> list[types.FunctionDeclaration]:
        return [self.convert(definition) for definition in definitions]

    def _build_schema(
        self,
        definition: ToolDefinition,
    ) -> types.Schema:
        properties: dict[str, types.Schema] = {}
        required: list[str] = []

        for parameter in definition.parameters:
            properties[parameter.name] = types.Schema(
                type=self._convert_type(parameter.type),
                description=parameter.description,
            )

            if parameter.required:
                required.append(parameter.name)

        return types.Schema(
            type=types.Type.OBJECT,
            properties=properties,
            required=required,
        )

    def _convert_type(
        self,
        parameter_type: ToolParameterType,
    ) -> types.Type:
        return self._TYPE_MAPPING[parameter_type]
