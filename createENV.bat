@echo off

echo Building venv
python -m venv venv
echo venv is built

call venv\Scripts\activate
echo venv is activated

pip install -r requirements.txt
echo Dependencies are installed for the project

echo Script completed

rem Pause to keep the command prompt window open
pause
