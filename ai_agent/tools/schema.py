from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ToolParameterType(str, Enum):
    STRING = "string"
    INTEGER = "integer"
    NUMBER = "number"
    BOOLEAN = "boolean"
    ARRAY = "array"
    OBJECT = "object"


@dataclass(frozen=True, slots=True)
class ToolParameter:
    name: str
    type: ToolParameterType
    description: str
    required: bool = True


@dataclass(frozen=True, slots=True)
class ToolDefinition:
    name: str
    description: str
    parameters: tuple[ToolParameter, ...] = ()
