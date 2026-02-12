# SISTEMA DE ORDENS DE SERVICO

## Procedimento

1. Extraia o arquivo ZIP
2. Clique duas vezes no start.bat conforme escolha
3. Aguarde abrir o navegador
4. Acesse: http://127.0.0.1:8000

## Requisitos:
- Python 3.11+ instalado




# Debug/Dev

habilitar venv PowerShell
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```
e para ativar na pasta que está o venv:
```bash
venv\Scripts\Activate.ps1
```

migrates:
```bash
python manage.py makemigrations
python manage.py migrate
```