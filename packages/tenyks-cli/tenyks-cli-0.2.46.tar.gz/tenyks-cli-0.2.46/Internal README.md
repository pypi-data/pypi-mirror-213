# Tenyks Command Line Interface

Contains Tenyks CLI module for uploading dataset and model.
## Setup
1. Install dependencies
```bash
make install-dev
```
2. Run command as found in `tenyks/__main__.py`

## Install
1. Install as package 
```bash
make install
```
1. run commands
```bash
tenyks dataset-create --name test
```

1. Install from test pypi
```bash
pip install -i https://test.pypi.org/simple/ tenyks-cli
```

## Build
```bash
make build
```

## Set up environment variables for pypi token 
Set the TEST_PYPI_KEY environment variable

## Deploy
```bash
make deploy-test
```