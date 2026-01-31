@echo off
echo Iniciando Sistema Oficina de Costura
echo.

REM -- Verifica se o Python está instalado
where python >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo Python nao encontrado!
    echo Por favor, instale o Python 3.x:
    start https://www.python.org/downloads/
    pause
    exit /b
)

cd oficina_costura

IF NOT EXIST venv (
    echo Criando ambiente virtual...
    python -m venv venv
)

call venv\Scripts\activate

IF NOT EXIST venv\.installed (
    echo Atualizando pip...
    pip install --upgrade pip

    echo Instalando dependencias...
    pip install -r requirements.txt

    echo ok > venv\.installed
)

echo Aplicando migrations...
python manage.py migrate

echo Coletando arquivos estaticos...
python manage.py collectstatic --noinput

REM -- Descobre IP local
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /C:"IPv4"') do set IP=%%a
set IP=%IP: =%

echo Abrindo navegador em http://%IP%:8000
start http://%IP%:8000

echo Subindo servidor...
python manage.py runserver 0.0.0.0:8000

pause
