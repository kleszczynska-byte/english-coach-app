# 🤖 Jak uruchomić English Coach z Claude Code

Claude Code to narzędzie CLI, które pozwala używać Claude bezpośrednio z terminala. Oto jak możesz użyć go do pracy z tą aplikacją:

## Co to jest Claude Code?

Claude Code to narzędzie wiersza poleceń, które umożliwia:
- Edycję wielu plików naraz
- Wykonywanie poleceń w terminalu
- Automatyzację zadań programistycznych
- Interaktywną pracę z kodem

## Instalacja Claude Code

```bash
# macOS/Linux
npm install -g @anthropic-ai/claude-code

# Lub używając npx (bez instalacji)
npx @anthropic-ai/claude-code
```

## Konfiguracja

```bash
# Ustaw klucz API
export ANTHROPIC_API_KEY="twój-klucz-api"

# Uruchom Claude Code
claude-code
```

## Jak Claude Code może pomóc z tą aplikacją?

### 1. Automatyczna instalacja i konfiguracja

```bash
# W katalogu projektu uruchom Claude Code
claude-code

# Następnie zapytaj:
"Zainstaluj wszystkie zależności backendu i frontendu, 
a następnie uruchom oba serwery"
```

Claude Code:
- Wykryje strukturę projektu
- Zainstaluje `pip install -r requirements.txt` dla backendu
- Zainstaluje `npm install` dla frontendu
- Uruchomi oba serwery

### 2. Debugowanie problemów

```bash
claude-code

# Zapytaj:
"Backend zwraca błąd 500 przy /analyze endpoint. 
Przeanalizuj logi i napraw problem."
```

Claude Code:
- Przeczyta kod backendu
- Sprawdzi logi
- Zaproponuje poprawki
- Zastosuje je automatycznie

### 3. Dodawanie nowych funkcji

```bash
claude-code

# Zapytaj:
"Dodaj funkcję eksportu rozmów do PDF w formacie raportu.
Użyj biblioteki reportlab."
```

Claude Code:
- Zainstaluje wymaganą bibliotekę
- Doda nowy endpoint do backendu
- Doda przycisk w frontendzie
- Przetestuje funkcjonalność

### 4. Refactoring i optymalizacja

```bash
claude-code

# Zapytaj:
"Przenieś kontekst użytkownika z pamięci do SQLite database.
Zachowaj kompatybilność z istniejącym API."
```

### 5. Tworzenie testów

```bash
claude-code

# Zapytaj:
"Napisz testy jednostkowe dla wszystkich endpointów API 
używając pytest"
```

## Przykładowe zadania dla Claude Code

### Szybki start projektu
```
"Zainicjuj projekt - zainstaluj zależności i uruchom serwery"
```

### Dodanie nowej funkcji
```
"Dodaj funkcjonalność zapamiętywania ulubionych fraz użytkownika"
```

### Fix błędów
```
"Napraw wszystkie błędy ESLint w kodzie frontendowym"
```

### Dokumentacja
```
"Wygeneruj dokumentację API w formacie OpenAPI/Swagger"
```

### Deployment
```
"Przygotuj Dockerfile i docker-compose.yml do łatwego deploymentu"
```

## Kiedy używać Claude Code vs zwykłego Claude?

**Użyj Claude Code gdy:**
- Musisz edytować wiele plików naraz
- Chcesz automatycznie instalować zależności
- Potrzebujesz uruchamiać komendy w terminalu
- Pracujesz nad dużymi refactoringami

**Użyj zwykłego Claude (claude.ai) gdy:**
- Potrzebujesz tylko porady
- Chcesz przeczytać dokumentację
- Planujesz architekturę
- Potrzebujesz wyjaśnienia koncepcji

## Przykładowa sesja z Claude Code

```bash
$ claude-code

Claude Code> Zainicjuj projekt English Coach

🔍 Analizuję strukturę projektu...
✅ Wykryto: Python backend (FastAPI) + React frontend (Vite)

📦 Instaluję zależności backendu...
✅ Zainstalowano: fastapi, uvicorn, anthropic, pydantic

📦 Instaluję zależności frontendu...
✅ Zainstalowano: react, vite, axios

🚀 Uruchamiam backend na porcie 8000...
✅ Backend działa: http://localhost:8000

🚀 Uruchamiam frontend na porcie 3000...
✅ Frontend działa: http://localhost:3000

🎉 Projekt gotowy! Otwórz http://localhost:3000 w przeglądarce.

Claude Code> Dodaj dark mode toggle w aplikacji

✍️  Edytuję App.jsx...
✍️  Edytuję App.css...
✅ Dodano przełącznik dark/light mode w headerze

Czy chcesz, żebym dodał także localStorage do zapamiętania preferencji?

Claude Code> Tak

✍️  Aktualizuję App.jsx z localStorage...
✅ Gotowe! Preferencje są teraz zapisywane.

Claude Code> exit
```

## Zaawansowane użycie

### Praca z API Anthropic w Claude Code

Claude Code używa tego samego API co aplikacja, więc może:
- Testować prompty dla coacha
- Eksperymentować z różnymi modelami Claude
- Optymalizować koszty przez użycie odpowiednich modeli

### Przykład: Testowanie różnych promptów

```bash
claude-code

# Zapytaj:
"Przetestuj 3 różne wersje system promptu dla coacha
i porównaj jakość odpowiedzi. Użyj przykładowej konwersacji 
z sample-transcripts.md"
```

## Koszty

Claude Code używa Anthropic API, więc kosztuje tyle samo co:
- Zwykłe API calls
- Dodatkowo: zazwyczaj więcej tokenów (czyta cały projekt)

**Wskazówka:** Dla małych projektów jak ten, koszt jest minimalny (~$0.50-2 na sesję).

## Troubleshooting Claude Code

### Błąd: "Cannot find claude-code"
```bash
# Zainstaluj globalnie
npm install -g @anthropic-ai/claude-code

# Lub używaj przez npx
npx @anthropic-ai/claude-code
```

### Błąd: "API key not found"
```bash
# Ustaw klucz API
export ANTHROPIC_API_KEY="sk-ant-..."

# Sprawdź czy jest ustawiony
echo $ANTHROPIC_API_KEY
```

### Claude Code nie widzi zmian w plikach
```bash
# Upewnij się, że jesteś w katalogu projektu
cd /ścieżka/do/english-coach-app

# Uruchom Claude Code
claude-code
```

## Podsumowanie

Claude Code to potężne narzędzie do:
- ✅ Szybkiej konfiguracji projektu
- ✅ Automatyzacji zadań developerskich  
- ✅ Debugowania i naprawiania błędów
- ✅ Dodawania nowych funkcjonalności
- ✅ Refactoringu kodu

Połączenie Claude Code (do kodowania) + English Coach App (do nauki) = 🚀 Maksymalna produktywność!
