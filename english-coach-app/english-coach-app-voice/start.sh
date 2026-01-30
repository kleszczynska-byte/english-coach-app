#!/bin/bash

echo "🎓 English Coach B2 - Quick Start"
echo "=================================="
echo ""

# Sprawdź czy klucz API jest ustawiony
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  BŁĄD: Brak klucza API Anthropic!"
    echo ""
    echo "Ustaw klucz przed uruchomieniem:"
    echo "export ANTHROPIC_API_KEY='twój-klucz-tutaj'"
    echo ""
    echo "Pobierz klucz z: https://console.anthropic.com/settings/keys"
    exit 1
fi

echo "✅ Klucz API wykryty"
echo ""

# Funkcja do uruchomienia backendu
start_backend() {
    echo "🔧 Uruchamiam backend..."
    cd backend
    
    # Sprawdź czy są zainstalowane zależności
    if ! python -c "import fastapi" 2>/dev/null; then
        echo "📦 Instaluję zależności backendu..."
        pip install -r requirements.txt --break-system-packages
    fi
    
    echo "🚀 Backend startuje na http://localhost:8000"
    python main.py &
    BACKEND_PID=$!
    cd ..
}

# Funkcja do uruchomienia frontendu
start_frontend() {
    echo "🔧 Uruchamiam frontend..."
    cd frontend
    
    # Sprawdź czy są zainstalowane zależności
    if [ ! -d "node_modules" ]; then
        echo "📦 Instaluję zależności frontendu..."
        npm install
    fi
    
    echo "🚀 Frontend startuje na http://localhost:3000"
    npm run dev &
    FRONTEND_PID=$!
    cd ..
}

# Funkcja czyszcząca
cleanup() {
    echo ""
    echo "🛑 Zatrzymywanie serwerów..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Uruchom oba serwery
start_backend
sleep 3
start_frontend

echo ""
echo "✅ Aplikacja uruchomiona!"
echo "📱 Otwórz przeglądarkę: http://localhost:3000"
echo ""
echo "Naciśnij Ctrl+C aby zatrzymać"
echo ""

# Czekaj
wait
