import logging as logger
import pathlib
import re
from datetime import datetime
from typing import Callable

import black
import isort
import yaml
from openapi3 import OpenAPI

from openapi_drf_codegen.utils.text_templates import (
    DEFAULT_COMMENT,
    INIT_TEMPLATE,
    PYPROJECT_TEMPLATE,
    README_TEXT,
)
from openapi_drf_codegen.utils.types import (
    Attribute,
    Import,
    OpenAPIFieldType,
    PyCode,
    Schema,
    SchemaType,
)

logger.basicConfig(level=logger.INFO, format="%(message)s")


class CodeGenerator:
    def __init__(self, openapi_path: str, package_name: str, package_version: str):
        self.openapi_path = openapi_path
        self.project_name = package_name
        self.package_name = self.project_name.replace("-", "_")
        self.package_version = package_version
        self.openapi = self._read_openapi()
        self.schemas = []
        self._enums = []
        self._schemas = []

    @property
    def readable_date(self) -> str:
        return datetime.now().strftime("%b %d, %Y at %H:%M:%S")

    @property
    def build_path(self) -> pathlib.Path:
        return pathlib.Path("build/")

    @property
    def project_path(self) -> pathlib.Path:
        return self.build_path

    @property
    def package_path(self) -> pathlib.Path:
        return pathlib.Path(self.project_path, self.package_name)

    @property
    def package_init_path(self) -> pathlib.Path:
        return pathlib.Path(self.serializers_path, "__init__.py")

    @property
    def readme_path(self) -> pathlib.Path:
        return pathlib.Path(self.project_path, "README.md")

    @property
    def serializers_path(self) -> pathlib.Path:
        return pathlib.Path(self.package_path, "serializers")

    def _read_openapi(self) -> OpenAPI:
        with open(self.openapi_path) as f:
            spec = yaml.safe_load(f.read())
        openapi = OpenAPI(spec)
        return openapi

    @staticmethod
    def _camel_to_snake(data: str) -> str:
        name = re.sub("((?<!^)([A-Z][a-z]+))", r"_\1", data)
        name = re.sub("([A-Z]+)", r"_\1", name)
        name = re.sub("__", "_", name)
        return name.lower().lstrip("_")

    def _add_pyproject(self):
        with open(pathlib.Path(self.project_path, "pyproject.toml"), "w") as file:
            file.write(
                PYPROJECT_TEMPLATE.format(
                    project_name=self.project_name,
                    version=self.package_version,
                    package_name=self.package_name,
                )
            )

    def _add_init_file(self):
        text = f"{INIT_TEMPLATE}\n\n{DEFAULT_COMMENT.format(current_date=self.readable_date)}"
        with open(self.package_init_path, "w") as file:
            file.write(text)

    def _add_readme_file(self):
        with open(self.readme_path, "w") as file:
            file.write(
                README_TEXT.format(
                    package_name=self.project_name, package_version=self.package_version
                )
            )

    def _init_build_package(self):
        self.serializers_path.mkdir(parents=True, exist_ok=True)
        self._add_init_file()
        self._add_readme_file()
        for schema_name, original_schema in self.openapi.components.schemas.items():
            snaked_schema_name = self._camel_to_snake(schema_name)
            file_name = f"{snaked_schema_name}.py"
            schema = Schema(
                camel_case_name=schema_name,
                snake_case_name=snaked_schema_name,
                schema=original_schema,
            )
            self.schemas.append(schema)
            pathlib.Path(self.serializers_path, file_name).touch(exist_ok=True)
        self._add_pyproject()

    @staticmethod
    def _get_schema_type(schema: Schema) -> str:
        if schema.schema.raw_element.get("properties"):
            return SchemaType.SCHEMA
        return SchemaType.ENUM

    @staticmethod
    def _squash_imports(imports: list[Import], attributes: list[Attribute]):
        required_imports = {
            imp
            for attribute in attributes
            if attribute.required_imports
            for imp in attribute.required_imports
        }
        return list(set(imports) | required_imports)

    def _write_code(self, code: PyCode):
        raw_code = DEFAULT_COMMENT.format(current_date=self.readable_date)
        imports = self._squash_imports(code.imports, code.attributes)
        for _import in imports:
            raw_code += f"{_import}\n"
        raw_code += "\n\n"
        raw_code += f"class {code.class_name}({code.inherit_from}):\n\n"
        for attribute in code.attributes:
            raw_code += f"    {attribute}\n"
        raw_code = black.format_str(raw_code, mode=black.FileMode())
        raw_code = isort.code(raw_code)
        with open(
            pathlib.Path(self.serializers_path, f"{code.file_name}.py"), "w"
        ) as file:
            file.write(raw_code)
        with open(self.package_init_path, "a") as file:
            file.write(f"from .{code.file_name} import {code.class_name}  # noqa \n")

    def _generate_enum(self, schema: Schema):
        imports = [
            Import("TextChoices", "django.db.models"),
        ]
        class_name = f"{schema.camel_case_name}Serializer"
        enum_values = schema.schema.raw_element.get(SchemaType.ENUM)
        attributes = [
            Attribute(name=value.upper(), value=f'"{value.lower()}", "{value.lower()}"')
            for value in enum_values
        ]
        code = PyCode(
            file_name=schema.snake_case_name,
            imports=imports,
            class_name=class_name,
            inherit_from=imports[0].import_what,
            attributes=attributes,
        )
        self._write_code(code)

    def _get_integer(self, field_name: str, field_data: dict) -> Attribute:
        allow_null = field_data.get("nullable") or False
        read_only = field_data.get("readOnly") or False
        help_text = field_data.get("description")
        args = f"allow_null={allow_null}, read_only={read_only}"
        if help_text:
            args += f', help_text="{help_text}"'
        attribute = Attribute(
            name=field_name, value=f"serializers.IntegerField({args})"
        )
        return attribute

    def _get_array(self, field_name: str, field_data: dict):
        allow_null = field_data.get("nullable") or False
        read_only = field_data.get("readOnly") or False
        help_text = field_data.get("description")
        args = f"allow_null={allow_null}, read_only={read_only}"
        if help_text:
            args += f', help_text="{help_text}"'
        array_items = field_data.get("items")
        items_type = array_items.get("type")
        if items_type:
            type_mapping = {
                OpenAPIFieldType.INTEGER: "serializers.IntegerField()",
                OpenAPIFieldType.STRING: "serializers.CharField()",
                OpenAPIFieldType.BOOLEAN: "serializers.BooleanField()",
                OpenAPIFieldType.NUMBER: "serializers.DecimalField(decimal_places=2, max_digits=2)",
            }
            attribute = Attribute(
                name=field_name,
                value=f"serializers.ListField(child={type_mapping.get(items_type)})",
            )
        else:
            item_schema = array_items.get("$ref").split("/")[-1]
            serializer_name = f"{item_schema}Serializer"
            imports = [Import(serializer_name, f".{self._camel_to_snake(item_schema)}")]
            if item_schema in self._enums:
                attribute = Attribute(
                    name=field_name,
                    value=f"serializers.ChoiceField(choices={serializer_name}.choices)",
                    required_imports=imports,
                )
            else:
                attribute = Attribute(
                    name=field_name,
                    value=f"{serializer_name}(many=True)",
                    required_imports=imports,
                )
        return attribute

    def _get_string(self, field_name: str, field_data: dict):
        max_length = field_data.get("maxLength")
        min_length = field_data.get("minLength")
        allow_null = field_data.get("nullable") or False
        read_only = field_data.get("readOnly") or False
        help_text = field_data.get("description")
        args = f"allow_null={allow_null}, read_only={read_only}"
        if help_text:
            args += f', help_text="{help_text}"'
        if max_length:
            args += f", max_length={max_length}"
        if min_length:
            args += f", min_length={min_length}"
        format = field_data.get("format")
        serializer_class_mapping = {
            "date-time": "serializers.DateTimeField",
            "uuid": "serializers.UUIDField",
            "date": "serializers.DateField",
            "email": "serializers.EmailField",
            "uri": "serializers.URLField",
            "ipv4": "serializers.IPAddressField",
            "ipv6": "serializers.IPAddressField",
        }
        serializer_name = serializer_class_mapping.get(format)
        if serializer_name:
            attribute = Attribute(
                name=field_name,
                value=f"{serializer_name}({args})",
            )
        else:
            attribute = Attribute(
                name=field_name, value=f"serializers.CharField({args})"
            )
        return attribute

    def _get_boolean(self, field_name: str, field_data: dict):
        help_text = field_data.get("description")
        args = ""
        if help_text:
            args += f'help_text="{help_text}"'
        attribute = Attribute(
            name=field_name, value=f"serializers.BooleanField({args})"
        )
        return attribute

    def _get_object(self, field_name: str, field_data: dict) -> Attribute:
        allow_null = field_data.get("nullable") or False
        read_only = field_data.get("readOnly") or False
        help_text = field_data.get("description")
        args = f"allow_null={allow_null}, read_only={read_only}"
        if help_text:
            args += f', help_text="{help_text}"'
        additional_properties = field_data.get("additionalProperties")
        if additional_properties:
            type = additional_properties.get("type")
            if type == OpenAPIFieldType.ARRAY:
                args += ", many=True"
                object_schema_name = (
                    additional_properties.get("items").get("$ref").split("/")[-1]
                )
                object_class_name = f"{object_schema_name}Serializer"
            else:
                object_schema_name = additional_properties.get("$ref").split("/")[-1]
                object_class_name = f"{object_schema_name}Serializer"
            imports = [
                Import(
                    object_class_name, f".{self._camel_to_snake(object_schema_name)}"
                )
            ]
            attribute = Attribute(
                name=field_name,
                value=f"{object_class_name}({args})",
                required_imports=imports,
            )
            return attribute

        else:
            attribute = Attribute(name=field_name, value="serializers.JSONField()")
            return attribute

    def _get_ref(self, field_name: str, field_data: dict) -> Attribute:
        schema_name = field_data.get("$ref").split("/")[-1]
        serializer_class_name = f"{schema_name}Serializer"
        imports = [
            Import(serializer_class_name, f".{self._camel_to_snake(schema_name)}")
        ]
        if schema_name in self._enums:
            attribute = Attribute(
                field_name,
                f"serializers.ChoiceField(choices={serializer_class_name}.choices)",
                required_imports=imports,
            )
        else:
            attribute = Attribute(
                field_name, f"{serializer_class_name}()", required_imports=imports
            )
        return attribute

    def _get_number(self, field_name: str, field_data: dict):
        allow_null = field_data.get("nullable") or False
        read_only = field_data.get("readOnly") or False
        help_text = field_data.get("description")
        args = f"allow_null={allow_null}, read_only={read_only}, decimal_places=2, max_digits=2"
        if help_text:
            args += f', help_text="{help_text}"'
        attribute = Attribute(
            name=field_name, value=f"serializers.DecimalField({args})"
        )
        return attribute

    def _get_all_of(self, field_name: str, field_data: dict):
        allow_null = field_data.get("nullable") or False
        read_only = field_data.get("readOnly") or False
        help_text = field_data.get("description")
        args = f"allow_null={allow_null}, read_only={read_only}"
        if help_text:
            args += f', help_text="{help_text}"'
        all_of = field_data.get("allOf")
        imports = []
        choices = []
        for ref in all_of:
            ref = ref.get("$ref")
            schema_name = ref.split("/")[-1]
            serializer_class_name = f"{schema_name}Serializer"
            imports.append(
                Import(serializer_class_name, f".{self._camel_to_snake(schema_name)}")
            )
            choices.append(serializer_class_name)
        choices = " + ".join(f"{choice}.choices" for choice in choices)
        attribute = Attribute(
            field_name,
            f"serializers.ChoiceField(choices={choices}, {args})",
            required_imports=imports,
        )
        return attribute

    def _get_class_attribute(
        self, schema_name: str, field_name: str, field_data: dict
    ) -> Attribute:
        if "type" in field_data:
            type = field_data.get("type").strip()
            method_name = f"_get_{type}"
            if hasattr(self, method_name):
                return getattr(self, method_name)(field_name, field_data)
        elif "$ref" in field_data:
            return self._get_ref(field_name, field_data)
        elif "allOf" in field_data:
            return self._get_all_of(field_name, field_data)
        logger.warning(
            f"Could not generate a field '{field_name}' for the '{schema_name}' serializer (functionality not implemented)"
        )

    def _generate_schema(self, schema: Schema):
        imports = [Import("serializers", "rest_framework")]
        class_name = f"{schema.camel_case_name}Serializer"
        properties = schema.schema.raw_element.get("properties")
        attributes = []
        for prop_name, prop_value in properties.items():
            attribute = self._get_class_attribute(
                schema.camel_case_name, prop_name, prop_value
            )
            if attribute:
                attributes.append(attribute)
        code = PyCode(
            file_name=schema.snake_case_name,
            imports=imports,
            class_name=class_name,
            inherit_from="serializers.Serializer",
            attributes=attributes,
        )
        self._write_code(code)

    def _generate_schema_code(self, schema: Schema):
        generator_method_mapping = {
            SchemaType.ENUM: self._generate_enum,
            SchemaType.SCHEMA: self._generate_schema,
        }
        schema.schema_type = self._get_schema_type(schema)
        required_method: Callable = generator_method_mapping.get(schema.schema_type)
        required_method(schema)

    def _sort_schemas(self):
        for schema in self.schemas:
            schema_type = self._get_schema_type(schema)
            if schema_type == SchemaType.ENUM:
                self._enums.append(schema.camel_case_name)
            else:
                self._schemas.append(schema.camel_case_name)

    def create_package(self):
        logger.info("Code generation started")
        self._init_build_package()
        self._sort_schemas()
        for schema in self.schemas:
            self._generate_schema_code(schema)
        logger.info(
            f"The package {self.package_name} with version {self.package_version} is generated in the 'build/' directory"
        )
