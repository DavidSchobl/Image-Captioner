@echo off
git pull
echo Activating virtual environment...
call .\venv\Scripts\activate

echo Running the application...
python Image_Captioner.py

echo Application has ended. Press any key to exit.
pause > nul
