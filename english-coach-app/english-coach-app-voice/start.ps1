# English Coach B2 - Quick Start (Windows)
Write-Host "🎓 English Coach B2 - Quick Start" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Sprawdź klucz API
if (-not $env:ANTHROPIC_API_KEY) {
    Write-Host "⚠️  BŁĄD: Brak klucza API Anthropic!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Ustaw klucz przed uruchomieniem:"
    Write-Host '$env:ANTHROPIC_API_KEY="twój-klucz-tutaj"' -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Pobierz klucz z: https://console.anthropic.com/settings/keys"
    exit 1
}

Write-Host "✅ Klucz API wykryty" -ForegroundColor Green
Write-Host ""

# Uruchom backend
Write-Host "🔧 Uruchamiam backend..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; pip install -r requirements.txt --break-system-packages; python main.py"

Start-Sleep -Seconds 5

# Uruchom frontend
Write-Host "🔧 Uruchamiam frontend..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm install; npm run dev"

Write-Host ""
Write-Host "✅ Aplikacja uruchamia się!" -ForegroundColor Green
Write-Host "📱 Za chwilę otwórz przeglądarkę: http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Zamknij okna PowerShell aby zatrzymać serwery" -ForegroundColor Gray
