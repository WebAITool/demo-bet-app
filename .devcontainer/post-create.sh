#!/bin/bash
set -e

echo "🛠️  Настройка Git..."
git config --global --add safe.directory /workspace

echo "🐍 Настройка Backend (uv)..."
cd backend
uv venv --allow-existing
uv pip install -r requirements-dev.txt

if ! grep -q 'source /workspace/backend/.venv/bin/activate' ~/.zshrc; then
    echo "📝 Добавляю активацию venv в .zshrc..."
    echo 'source /workspace/backend/.venv/bin/activate' >> ~/.zshrc
fi

echo "☕ Настройка Frontend (npm)..."
cd ../frontend
npm install

echo "✅ Готово! Окружение настроено."
