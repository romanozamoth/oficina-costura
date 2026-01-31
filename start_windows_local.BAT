@echo off
echo Iniciando Sistema Oficina de Costura

REM -- Verifica se o Python está instalado
where python >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo Python nao encontrado!
    echo Por favor, instale o Python 3.x: https://www.python.org/downloads/
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

echo Atualizando pip...
pip install --upgrade pip

echo Instalando dependencias...
pip install -r requirements.txt

echo Aplicando migrations...
python manage.py migrate

echo Coletando arquivos estaticos...
python manage.py collectstatic --noinput

echo Abrindo navegador...
start http://127.0.0.1:8000

echo Subindo servidor...
python manage.py runserver

pause
