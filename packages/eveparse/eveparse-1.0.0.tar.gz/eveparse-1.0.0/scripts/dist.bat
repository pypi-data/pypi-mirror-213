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

:: Build tar.gz and whl
python -m build

:: Upload to PyPI
python -m twine upload dist/*

:: Delete dist/
rmdir /S /Q dist
