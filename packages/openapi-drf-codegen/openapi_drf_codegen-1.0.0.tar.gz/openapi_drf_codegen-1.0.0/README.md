# OpenAPI DRF Codegen

### CLI application for generating DRF serializers from openapi.yaml files

###  NOTE: This program was mostly written for personal use. You may also find it useful

**Installation**:

```bash
pip install openapi-drf-codegen

# or

poetry add openapi-drf-codegen
```

**Usage**:

```bash
openapi-drf-codegen -i /path/to/openapi/ -p package-name -v 0.0.1
```

A new 'build' directory will be created in your directory where you are. To build a python package for installation, you can do the following:

```bash
cd build/ && poetry build
```

### Important: at the moment, the generator does not provide all possible cases for code generation. Maybe I'll add them in the future if I find them

## Contribution

### If you want to participate in the project and fix some details or add functionality - feel free to contribute
