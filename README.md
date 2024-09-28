# Smart Task Manager API Solution


- get inputs
- validate inputs
- logging
- database queries
- check database response (success vs. failure)
- http response
    - standardized messaging in response
    - error responses
    - success responses
- browsable API documentation


- Installation
- Configuration
- Live reload
- Task runner
- Code generation
- Debugging
- Testing

## Dependencies

- Flask: micro-framework for building APIs
- schematics: validation
- psycopg2: PostgreSQL
- cassandra-python: Cassandra
- annotated-types
- anyio
- asarPy
- blinker
- certifi
- charset-normalizer
- click
- distro
- filelock
- Flask
- Flask-SQLAlchemy
- fsspec
- greenlet
- h11
- httpcore
- httpx
- huggingface-hub
- idna
- itsdangerous
- Jinja2
- jiter
- MarkupSafe
- numpy
- openai
- packaging
- pydantic
- pydantic_core
- PyYAML
- regex
- requests
- safetensors
- SQLAlchemy
- tokenizers
- tqdm
- transformers
- typing_extensions 
- urllib3
- Werkzeug

## Steps

- Install Python
- Install Vs Code
- Install virtualenv/virtualenvwrapper

```bash
pip install -r requirements.txt
```

## Start/stop server

```bash
flask --app app run --debug
```

## Files

`./app.py`
`./README.txt`
`./requirements.txt`

