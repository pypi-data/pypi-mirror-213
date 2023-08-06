PYPROJECT_TEMPLATE = (
    "[tool.poetry]\n"
    'name = "{project_name}"\n'
    'version = "{version}"\n'
    'description = "Automatically generated serializers for DRF based on OpenAPI file"\n'
    'authors = ["OpenAPI DRF Codegen"]\n'
    'readme = "README.md"\n'
    'packages = [{{include = "{package_name}"}}]\n\n'
    "[tool.poetry.dependencies]\n"
    'python = "^3.8"\n'
    'djangorestframework = "^3.14.0"\n\n'
    "[build-system]\n"
    'requires = ["poetry-core"]\n'
    'build-backend = "poetry.core.masonry.api"'
)


INIT_TEMPLATE = r"""
#     ____   ____   ______ _   __ ___     ____   ____
#    / __ \ / __ \ / ____// | / //   |   / __ \ /  _/
#   / / / // /_/ // __/  /  |/ // /| |  / /_/ / / /
#  / /_/ // ____// /___ / /|  // ___ | / ____/_/ /
#  \____//_/    /_____//_/ |_//_/  |_|/_/    /___/
#
#      ____   ____   ______
#     / __ \ / __ \ / ____/
#    / / / // /_/ // /_
#   / /_/ // _, _// __/
#  /_____//_/ |_|/_/
#
#     ______ ____   ____   ______ ______ ______ _   __
#    / ____// __ \ / __ \ / ____// ____// ____// | / /
#   / /    / / / // / / // __/  / / __ / __/  /  |/ /
#  / /___ / /_/ // /_/ // /___ / /_/ // /___ / /|  /
#  \____/ \____//_____//_____/ \____//_____//_/ |_/
#
"""


DEFAULT_COMMENT = (
    "#  This code was generated automatically by openapi-django-codegen on {current_date}\n"
    "#  Do not edit this code manually\n\n"
)

README_TEXT = "# {package_name}\n\n### Automatically generated serializers for DRF. Package version: {package_version}"
