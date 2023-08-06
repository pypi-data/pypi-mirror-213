import string
from dataclasses import dataclass

from openapi3.schemas import Schema as OpenAPISchema


class SchemaType:
    SCHEMA = "schema"
    ENUM = "enum"


@dataclass
class Schema:
    camel_case_name: str
    snake_case_name: str
    schema: OpenAPISchema
    schema_type: str | None = None


@dataclass
class Import:
    import_what: str
    import_from: str | None

    def __str__(self):
        if self.import_from:
            return f"from {self.import_from} import {self.import_what}"
        return f"import {self.import_what}"

    def __hash__(self):
        return hash((self.import_what, self.import_from))


@dataclass
class Attribute:
    name: str
    value: str
    required_imports: list[Import] | None = None

    def __str__(self):
        return f"{self.name} = {self.value}"

    def __post_init__(self):
        allowed_first_chars = string.ascii_lowercase + string.ascii_uppercase + "_"
        allowed_chars = allowed_first_chars + string.digits
        if self.name[0] not in allowed_first_chars:
            self.name = f"_{self.name}"
        self.name = "".join(
            char if char in allowed_chars else "_" for char in self.name
        )


@dataclass
class PyCode:
    file_name: str
    imports: list[Import]
    class_name: str
    inherit_from: str
    attributes: list[Attribute]


class OpenAPIFieldType:
    INTEGER = "integer"
    ARRAY = "array"
    STRING = "string"
    BOOLEAN = "boolean"
    OBJECT = "object"
    NUMBER = "number"
