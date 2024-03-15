@echo off
echo Creating virtual environment...
python -m venv venv
echo Virtual environment created.

echo Activating virtual environment...
call .\venv\Scripts\activate

echo Installing required libraries from requirements.txt...
pip install -r requirements.txt
echo All required libraries were successfully installed.

pause
