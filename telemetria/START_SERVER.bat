@echo off
echo Limpando cache...
del /S /Q __pycache__ 2>nul

echo.
echo Iniciando servidor Django...
python manage.py runserver

pause
