# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2023-06-12

### Added

- automatic testing on push/pull to main/develop branches
- editor configuration
- flake8 configuration
- lint script
- linting with black, flake8, isort
- ViewContents parser

### Changed

- updated import ordering found by linter
- removed unused import in __init__.py
- sde.py no longer writes intermediate CSV to file.

### Deprecated

- support for Python <3.9

[unreleased]: https://github.com/harrelchris/eveparse/compare/main...develop
