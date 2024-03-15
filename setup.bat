
@echo off
echo Creating virtual environment...
python -m venv venv
echo Virtual environment created.

echo Activating virtual environment...
.env\Scriptsctivate

echo Installing required libraries...
pip install -r requirements.txt
echo Installation completed.

pause
