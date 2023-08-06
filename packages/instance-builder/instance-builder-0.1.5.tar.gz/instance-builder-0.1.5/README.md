# Instance-Builder - Instance builder library for Python inspired by Lombok

![Python Versions](https://img.shields.io/pypi/pyversions/instance-builder.svg)
![PyPI version](https://badge.fury.io/py/instance-builder.svg)
![CI](https://github.com/shimech/instance-builder/actions/workflows/test.yml/badge.svg)

## Installation

```shell
pip install instance-builder
```

## Usage

```python
@builder("id", "name", "age", "email")
class User:
    def __init__(self, id: int, name: str, age: int, email: str) -> None:
        self.id = id
        self.name = name
        self.age = age
        self.email = email

user = User.Builder().id(0).name("Shuntaro Shimizu").age(99).email("ut.s.shimizu@gmail.com").build()
```

© Copyright 2021 to Shuntaro Shimizu, under the MIT license
