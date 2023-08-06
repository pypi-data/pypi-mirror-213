# nacos-sdk-rust-binding-py
nacos-sdk-rust binding for Python with PyO3.

Tip: nacos-sdk-python 仓库暂未提供 2.x gRPC 交互模式，为了能升级它，故而通过 ffi 方式调用 nacos-sdk-rust

## Installation

```bash
pip install nacos_sdk_rust_binding_py
```

# Usage
- TODO

## Development

Setup virtualenv:

```shell
python -m venv venv
```

Activate venv:

```shell
source venv/bin/activate
````

Install `maturin`:

```shell
pip install maturin[patchelf]
```

Build bindings:

```shell
maturin develop
```

Run some tests:

```shell
maturin develop -E test
behave tests
```

Build API docs:

```shell
maturin develop -E docs
pdoc nacos_sdk_rust_binding_py
```

# License
[Apache License Version 2.0](LICENSE)

# Acknowledgement
- binding for Python with [PyO3](https://github.com/PyO3/pyo3.git)
- binding the [nacos-sdk-rust](https://github.com/nacos-group/nacos-sdk-rust.git)
