@echo off
echo Ativando ambiente virtual...
call .venv\Scripts\activate.bat

echo.
echo Definindo variaveis de ambiente...
set PYTHONDONTWRITEBYTECODE=1

echo.
echo Iniciando servidor Django...
python manage.py runserver

pause
