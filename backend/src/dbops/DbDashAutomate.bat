@echo off

REM Parameters
REM === Log file path ===
REM %1 = job_id

set JOB_ID=%1
REM LOGFILE=C:\Users\PIDVISCXADMINP\Desktop\dba-workspace\DbDashAutomation\automation.log
set LOGFILE=automation.log

REM Change directory to your project folder where the venv is
cd /d "C:\Users\PIDVISCXADMINP\Desktop\dba-workspace\DbDashAutomation"

echo Script started at %DATE% %TIME% >> "%LOGFILE%"
echo ----------------------------- >> "%LOGFILE%"
echo Job %JOB_ID% >> "%LOGFILE%"

REM Activate the virtual environment
call venv\Scripts\activate.bat

REM Run your Python script (adjust the script path)
python dbdashpro.py -j %JOB_ID% >> "%LOGFILE%"

echo ----------------------------- >> "%LOGFILE%"
echo Script finished at %DATE% %TIME% >> "%LOGFILE%"

REM Deactivate the virtual environment
deactivate