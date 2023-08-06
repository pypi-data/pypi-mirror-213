@echo off

:: Create virtual environment
if not exist .venv\ (
	python -m venv .venv
)

:: Activate virtual environment
if not defined VIRTUAL_ENV (
	call .venv\Scripts\activate
)

:: Update virtual environment
python -m pip install --upgrade pip setuptools wheel twine build

python -m build

python -m twine upload dist/*
