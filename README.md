# 🎓 English Coach B2 - Aplikacja do nauki angielskiego dla Implementation Specialists

Inteligentna aplikacja do nauki angielskiego B2 w kontekście pracy wdrożeniowca, wykorzystująca Claude AI.

## ✨ Funkcjonalności

### 📝 Analiza Materiałów
- Wklejasz transkrypcje rozmów z klientami lub opisy swoich obowiązków
- Claude **automatycznie wydobywa słownictwo** i identyfikuje tematy
- **Rozszerza kontekst** - nie ogranicza się tylko do podanych słów, proponuje powiązane tematy
- Buduje bazę wiedzy o Twoim słownictwie branżowym

### 💬 Interaktywne Rozmowy
- Prowadzisz konwersacje PO ANGIELSKU z AI coachem
- Coach symuluje scenariusze z pracy: kickoff meetings, client calls, technical discussions
- **Korekta na bieżąco** - błędy są wskazywane i wyjaśniane
- Rozmowa dostosowana do poziomu B2 i Twojej branży

### 🧠 Zarządzanie Kontekstem
- Przeglądasz zgromadzone słownictwo i tematy
- Śledzisz liczbę materiałów i rozmów
- Możesz wyczyścić kontekst i zacząć od nowa

### 📊 Analiza Postępów
- Generujesz raporty o swoich mocnych stronach
- Otrzymujesz konkretne rekomendacje co ćwiczyć
- Śledzisz rozwój w czasie

## 🚀 Instalacja i Uruchomienie

### Wymagania
- Python 3.9+
- Node.js 18+
- Klucz API Anthropic (Claude)

### Krok 1: Pozyskaj klucz API Anthropic

1. Zarejestruj się na https://console.anthropic.com/
2. Przejdź do sekcji "API Keys"
3. Wygeneruj nowy klucz API
4. **Skopiuj klucz** - będzie potrzebny w kolejnych krokach

### Krok 2: Backend (FastAPI)

```bash
# Wejdź do katalogu backend
cd backend

# Zainstaluj zależności
pip install -r requirements.txt --break-system-packages

# WAŻNE: Ustaw klucz API
export ANTHROPIC_API_KEY="twój-klucz-api-tutaj"

# Dla Windows (PowerShell):
# $env:ANTHROPIC_API_KEY="twój-klucz-api-tutaj"

# Uruchom serwer
python main.py
```

Backend będzie działał na: `http://localhost:8000`

### Krok 3: Frontend (React)

```bash
# Otwórz nowy terminal i wejdź do katalogu frontend
cd frontend

# Zainstaluj zależności
npm install

# Uruchom aplikację
npm run dev
```

Frontend będzie działał na: `http://localhost:3000`

### Krok 4: Otwórz aplikację

Przejdź do przeglądarki: **http://localhost:3000**

---

## 📖 Jak używać aplikacji?

### 1️⃣ **Zacznij od Analizy**

Przejdź do zakładki **"📝 Analiza"** i wklej:

**Przykład transkrypcji:**
```
During yesterday's kickoff meeting with the client, we discussed 
the implementation roadmap for their new CRM system. They need 
to migrate data from their legacy platform and integrate with 
their existing marketing automation tools. We agreed on a 
phased approach with weekly status updates.
```

**Przykład opisu:**
```
I'm an Implementation Specialist at a SaaS company. My main 
responsibilities include: leading client onboarding sessions, 
configuring system integrations, troubleshooting technical 
issues, and providing training to end users.
```

Kliknij **"🚀 Analizuj"** - Claude wydobędzie słownictwo i automatycznie rozszerzy tematy!

### 2️⃣ **Rozpocznij Rozmowę**

Przejdź do zakładki **"💬 Rozmowa"** i zacznij pisać PO ANGIELSKU:

**Przykłady pierwszych wiadomości:**
- `"Hi! Yesterday we had a kickoff meeting with a new client..."`
- `"I'm facing an integration issue with the API..."`
- `"Can we practice a status update call?"`

Coach odpowie, **skoryguje błędy** jeśli je zrobisz, i poprowadzi konwersację!

### 3️⃣ **Sprawdź Kontekst**

Zakładka **"🧠 Kontekst"** pokazuje:
- Ile słów i tematów aplikacja zna o Twojej pracy
- Pełną listę terminów
- Statystyki

### 4️⃣ **Generuj Raport Postępów**

Zakładka **"📊 Postępy"**:
- Kliknij **"📈 Generuj raport"**
- Otrzymasz analizę swoich mocnych stron
- Konkretne obszary do poprawy
- Rekomendacje dalszej nauki

---

## 🎯 Przykładowe Scenariusze Rozmów

Coach może ćwiczyć z Tobą:

### 🚀 Kickoff Meeting
```
Coach: "Let's simulate a kickoff meeting. Imagine I'm your new 
client. Tell me about the implementation process."
```

### 🔧 Troubleshooting
```
You: "The API integration is not working correctly"
Coach: [koryguje błędy] "Can you describe what error message 
you're seeing? Have you checked the authentication credentials?"
```

### 📊 Status Update
```
Coach: "Give me a status update on the project. What's completed 
and what are the blockers?"
```

### 💼 Stakeholder Management
```
Coach: "The client is concerned about the timeline. How would 
you address their concerns?"
```

---

## 🔧 Rozwiązywanie Problemów

### Backend nie startuje
**Problem:** `ANTHROPIC_API_KEY not configured`
**Rozwiązanie:** Upewnij się, że ustawiłeś klucz API:
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
python main.py
```

### Frontend nie może połączyć się z backendem
**Sprawdź:**
1. Czy backend działa na porcie 8000? (`http://localhost:8000`)
2. Czy w konsoli są błędy CORS?
3. Zrestartuj oba serwery

### Claude zwraca błędy
**Możliwe przyczyny:**
- Brak środków na koncie Anthropic
- Nieważny klucz API
- Problem z siecią

**Sprawdź saldo:** https://console.anthropic.com/settings/billing

---

## 💡 Dodatkowe Informacje

### Ceny API Anthropic (Claude Sonnet 4)
- ~$3 za milion input tokens
- ~$15 za milion output tokens
- Typowa sesja nauki (~20 wymian): **~$0.10 - $0.30**

### Bezpieczeństwo
- Klucz API **nie jest zapisywany** w plikach aplikacji
- Jest przekazywany tylko przez zmienną środowiskową
- **NIGDY** nie commituj klucza do Git!

### Rozbudowa Aplikacji
Możesz dodać:
- Bazę danych (SQLite/PostgreSQL) do trwałego zapisywania kontekstu
- Autentykację użytkowników
- Export rozmów do PDF
- Integrację z Whisper API (transkrypcja audio)
- Text-to-Speech (słuchanie odpowiedzi)

---

## 📁 Struktura Projektu

```
english-coach-app/
├── backend/
│   ├── main.py           # FastAPI server + logika biznesowa
│   └── requirements.txt   # Zależności Python
├── frontend/
│   ├── src/
│   │   ├── App.jsx       # Główny komponent React
│   │   ├── App.css       # Style
│   │   └── main.jsx      # Punkt wejścia
│   ├── index.html        # HTML template
│   ├── package.json      # Zależności npm
│   └── vite.config.js    # Konfiguracja Vite
└── README.md             # Ta dokumentacja
```

---

## 🤝 Wsparcie

Jeśli masz pytania lub problemy:
1. Sprawdź dokumentację Anthropic: https://docs.anthropic.com/
2. Przeczytaj sekcję "Rozwiązywanie Problemów" powyżej
3. Sprawdź logi w konsoli backendu i frontendu

---

## 📝 Licencja

Projekt jest darmowy do użytku osobistego. Pamiętaj o kosztach API Anthropic.

---

**Powodzenia w nauce angielskiego! 🎉**

_Zbudowane z ❤️ przy użyciu Claude AI_
