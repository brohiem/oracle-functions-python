# Oracle Functions Python — Hello World

A minimal Python serverless function built on the [Fn Project](https://fnproject.io/) for Oracle Cloud Infrastructure (OCI) Functions.

## What it does

Accepts a JSON payload with an optional `name` field and returns a greeting:

```json
// Request
{"name": "Alice"}

// Response
{"message": "Hello Alice"}
```

If no name is provided, it defaults to `"Hello World"`.

## Prerequisites

- [Fn CLI](https://github.com/fnproject/cli) installed
- Python 3.11+
- An OCI Functions application (for cloud deployment)

## Project structure

```
├── func.py            # Function handler
├── func.yaml          # Fn project configuration
├── requirements.txt   # Python dependencies
└── test_func.py       # Unit tests
```

## Local development

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the tests:

```bash
python -m pytest test_func.py -v
```

## Deploy to OCI Functions

```bash
fn deploy --app <your-app-name>
```

## Invoke

```bash
echo '{"name": "Alice"}' | fn invoke <your-app-name> helloworld-func-python
```
