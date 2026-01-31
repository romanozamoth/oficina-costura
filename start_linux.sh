#!/bin/bash

echo "🚀 Iniciando sistema Oficina de Costura"

cd oficina_costura || exit

if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual"
    python3 -m venv venv
fi

source venv/bin/activate

echo "⬆️ Atualizando pip"
pip install --upgrade pip

echo "📚 Instalando dependências"
pip install -r requirements.txt

echo "🗄️ Aplicando migrations"
python manage.py migrate

echo "🎨 Coletando arquivos estáticos"
python manage.py collectstatic --noinput

echo "🌐 Abrindo navegador"
xdg-open http://127.0.0.1:8000 >/dev/null 2>&1 &

echo "▶️ Subindo servidor"
python manage.py runserver
