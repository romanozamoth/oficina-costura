SISTEMA DE ORDENS DE SERVICO

1. Extraia o arquivo ZIP
2. Clique duas vezes em start.bat
3. Aguarde abrir o navegador
4. Acesse: http://127.0.0.1:8000

Requisitos:
- Windows
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