@echo off

:: Activate virtual environment
if not defined VIRTUAL_ENV (
	call .venv\Scripts\activate
)

:: isort
python -m isort eveparse --profile black

:: Flake8
python -m flake8 eveparse

:: Black
python -m black eveparse
