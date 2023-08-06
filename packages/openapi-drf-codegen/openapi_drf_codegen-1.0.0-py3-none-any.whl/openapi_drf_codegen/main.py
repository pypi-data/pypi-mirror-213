import click

from openapi_drf_codegen.codegen import CodeGenerator


@click.command()
@click.option(
    "-i",
    "--input-file",
    required=True,
    type=click.Path(exists=True),
    help="OpenAPI file path",
)
@click.option("-p", "--package-name", required=True, type=str, help="Package name")
@click.option("-v", "--version", required=True, type=str, help="Package version")
def main(input_file: str, package_name: str, version: str):
    generator = CodeGenerator(input_file, package_name, version)
    generator.create_package()


if __name__ == "__main__":
    main()
