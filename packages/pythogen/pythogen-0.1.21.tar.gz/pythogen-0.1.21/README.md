<div>
  <p align="center">
    <img src="docs/images/logo_long.png" height="auto" width="400px">
  </p>
  <br/>
</div>

Generator of python HTTP-clients from OpenApi specification based on [httpx](https://github.com/projectdiscovery/httpx) and [pydantic](https://github.com/pydantic/pydantic).

[![Build Status](https://github.com/artsmolin/pythogen/actions/workflows/main.yml/badge.svg)](https://github.com/artsmolin/pythogen/actions)
[![codecov](https://codecov.io/gh/artsmolin/pythogen/branch/main/graph/badge.svg?token=6JR6NB8Y9Z)](https://codecov.io/gh/artsmolin/pythogen)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[![Python](https://img.shields.io/pypi/pyversions/pythogen.svg)](https://pypi.python.org/pypi/pythogen/)
[![pypi](https://img.shields.io/pypi/v/pythogen.svg)](https://pypi.org/project/pythogen/)

[![license](https://img.shields.io/github/license/artsmolin/pythogen.svg)](https://github.com/artsmolin/pythogen/blob/master/LICENSE)

---

<p align="center">
  <img src="docs/images/example.png">
</p>

## Features
- [Discriminator](/docs/discriminator.md)
- [Metrics](/docs/metrics.md)
- [Logs](/docs/logs.md)
- [Required Headers](/docs/headers.md)
- Sync/async clients

## Examples
- [**Petstore OpenAPI**](/examples/petstore/openapi.yaml):  [client_sync.py](/examples/petstore/client_sync.py) | [client_async.py](/examples/petstore/client_async.py)

## Installation
```shell
pip install pythogen
```

## Usage
### Generate ordinary clients
- Asynchronous client
  ```shell
  pythogen path/to/input/openapi.yaml path/to/output/client.py
  ```
- Asynchronous client with integration for metrics
  ```shell
  pythogen path/to/input/openapi.yaml path/to/output/client.py --metrics
  ```
- Synchronous client
  ```shell
  pythogen path/to/input/openapi.yaml path/to/output/client.py --sync
  ```
- Synchronous client with integration for metrics
  ```shell
  pythogen path/to/input/openapi.yaml path/to/output/client.py --sync --metrics
  ```
### Generate client as python-package
```shell
pythogen path/to/input/openapi.yaml path/to/package/output --package-version=0.0.1 --package-authors="Rick, Morty"
```
- `--package-version` — required;
- `--package-authors` — optional;
- `path/to/package/output` — path to the directory where package will be saved.
### Usage client
```python
from petstore.client_async import Client
from petstore.client_async import Pet
from petstore.client_async import EmptyBody

client = Client(base_url="http://your.base.url")
pets: list[Pet] | EmptyBody = await client.findPetsByStatus(status="available")
```

[Development](/docs/development.md)
