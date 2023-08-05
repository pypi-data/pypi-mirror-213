# ![icon](https://github.com/kokseen1/toori/blob/master/toori/icon.png?raw=true) toori 

[![PyPI Release](https://github.com/kokseen1/toori/actions/workflows/release.yml/badge.svg)](https://github.com/kokseen1/toori/actions/workflows/release.yml)
[![PyPI Version](https://img.shields.io/pypi/v/toori.svg)](https://pypi.python.org/pypi/toori/)

A minimal layer 3 tunnel over http(s).

## Prerequisites

- [MSVC Build Tools](https://visualstudio.microsoft.com/downloads/)

## Installation

```
pip install toori
```

## Usage

Run as Administrator:

```shell
toori <server address>
```

### Examples

```shell
toori https://toori.server
```

Don't tunnel DNS requests

```shell
toori https://toori.server -nd
```

Only tunnel SSH traffic

```shell
toori https://toori.server -f "tcp.DstPort == 22"
```
