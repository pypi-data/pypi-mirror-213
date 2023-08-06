# aws-ecs-exec

[![pypi-version]][pypi]

A cli tool to conveniently execute commands in AWS ECS Tasks.

## Requirements

- Python 3.10+
- AWS CLI

The tool assumes that the `aws` command is installed on your path.

## Installation

Install using `pip`

```sh
pip install aws-ecs-exec
```

## Usage

Quickstart:

```sh
$ ecs-exec
```

For help:

```sh
$ ecs-exec --help
```

## Known issues

- This has been developed and only tested on MacOS.
- No pagination is used with boto3 calls, so there will likely be errors
  if page limits are exceeded.
- Does not support tasks with multiple containers.

[pypi-version]: https://img.shields.io/pypi/v/aws-ecs-exec.svg
[pypi]: https://pypi.org/project/aws-ecs-exec/
