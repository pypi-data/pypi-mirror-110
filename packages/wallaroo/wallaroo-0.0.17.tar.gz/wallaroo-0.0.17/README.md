# Python SDK for Wallaroo


This repo contains the python SDK used to interface with the Wallaroo API. The structure is as follows:

- Package name: Wallaroo
- Modules contained: sdk
- [SDK documentation](https://wallaroolabs.github.io/wallaroo-docs/sdk.html)

## Tests
To execute all tests run:
```sh
python -m unittest discover
```
To execute a specific test run:
```sh
python -m tests.test_name
```
Example:
```sh
python -m tests.test_smoke
```

## Build

Make sure you have the latest version of 'build'
```sh
make build-sdk
```
This will generate a distribution package in the dist directory.

## Generate Documentation

pdoc3 is used to generate the documentation for the SDK.
To generate the documentation run:
```sh
make doc
```
This will generate documentation files in the [html](html) directory


To remove generated files:
```sh
make clean
```
