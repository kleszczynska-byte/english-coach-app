# ⚡ QUICKSTART - 5 minut do uruchomienia

## 🎯 Co otrzymujesz?

Aplikację webową do nauki angielskiego B2 dla wdrożeniowców:
- 💬 Rozmowy z AI w kontekście Twojej pracy
- 📝 Automatyczna analiza słownictwa z transkrypcji
- ✅ Korekta błędów na bieżąco
- 📊 Raporty postępów

## ⚡ Szybki start (3 kroki)

### 1️⃣ Pobierz klucz API Anthropic (2 minuty)

1. Wejdź na: https://console.anthropic.com/
2. Zarejestruj się (możesz użyć Google)
3. Kliknij "Get API Keys"
4. Kliknij "Create Key"
5. **SKOPIUJ KLUCZ** (zaczyna się od `sk-ant-`)

💡 **Dostaniesz $5 kredytu gratis!** To wystarczy na ~50 sesji nauki.

### 2️⃣ Uruchom backend (1 minuta)

```bash
# Wejdź do katalogu projektu
cd english-coach-app/backend

# Ustaw klucz API (wklej swój klucz)
export ANTHROPIC_API_KEY="sk-ant-twój-klucz-tutaj"

# Zainstaluj i uruchom
pip install -r requirements.txt --break-system-packages
python main.py
```

✅ Backend działa na: `http://localhost:8000`

### 3️⃣ Uruchom frontend (1 minuta)

**Otwórz nowy terminal:**

```bash
cd english-coach-app/frontend

# Zainstaluj i uruchom
npm install
npm run dev
```

✅ Frontend działa na: `http://localhost:3000`

## 🎉 Gotowe! Otwórz: http://localhost:3000

---

## 🚀 Pierwsze kroki w aplikacji

### Krok 1: Dodaj kontekst swojej pracy

1. Kliknij zakładkę **"📝 Analiza"**
2. Otwórz plik `sample-transcripts.md` 
3. Skopiuj jedną z przykładowych transkrypcji
4. Wklej do aplikacji
5. Kliknij **"🚀 Analizuj"**

✨ Claude automatycznie wydobędzie słownictwo i **rozszerzy tematy**!

### Krok 2: Zacznij rozmowę

1. Przejdź do zakładki **"💬 Rozmowa"**
2. Napisz coś po angielsku, np.:
   ```
   Hi! Yesterday we had a kickoff meeting with new client. 
   They want migrate their data to cloud.
   ```
3. Naciśnij Enter

🤖 Coach odpowie, **skoryguje błędy** i będzie rozwijał rozmowę!

### Krok 3: Zobacz postępy

Po kilku rozmowach:
1. Przejdź do zakładki **"📊 Postępy"**
2. Kliknij **"📈 Generuj raport"**

📈 Dostaniesz analizę mocnych stron i rekomendacje!

---

## 🆘 Problemy?

### "Backend nie startuje"
```bash
# Sprawdź czy ustawiłeś klucz API
echo $ANTHROPIC_API_KEY

# Powinien wypisać: sk-ant-...
# Jeśli nie, ustaw go ponownie
```

### "Frontend pokazuje błąd połączenia"
```bash
# Sprawdź czy backend działa:
curl http://localhost:8000

# Powinno zwrócić JSON z "message": "English Coach API is running"
```

### "Brak środków na koncie Anthropic"
- Sprawdź saldo: https://console.anthropic.com/settings/billing
- Dodaj kartę lub użyj kredytu startowego ($5)

---

## 💰 Ile to kosztuje?

**Modele Claude Sonnet 4:**
- ~$3 za 1M input tokens
- ~$15 za 1M output tokens

**Praktycznie:**
- 1 sesja nauki (20 wymian): **$0.10 - $0.30**
- Analiza transkrypcji: **$0.05 - $0.10**
- Raport postępów: **$0.05**

**Kredyt $5 = około 30-50 sesji nauki!** 🎉

---

## 📚 Co dalej?

1. **Przeczytaj `README.md`** - pełna dokumentacja
2. **Użyj `sample-transcripts.md`** - przykładowe materiały do analizy
3. **Zobacz `CLAUDE_CODE_GUIDE.md`** - jak używać Claude Code do rozwoju aplikacji

---

## 🎓 Przykładowe tematy rozmów

Możesz ćwiczyć:

- 🚀 **Kickoff meetings**: "Let's simulate a kickoff with a new client..."
- 🔧 **Troubleshooting**: "I'm facing an API integration issue..."
- 📊 **Status updates**: "Give me an update on the project..."
- 💼 **Client communication**: "The client is concerned about the timeline..."
- 👥 **Team standups**: "Here's my update from yesterday..."

Coach będzie prowadzić rozmowę i **korygować błędy** na bieżąco!

---

## ⚙️ Dla zaawansowanych

### Automatyczne uruchomienie (Linux/Mac)
```bash
chmod +x start.sh
./start.sh
```

### Automatyczne uruchomienie (Windows)
```powershell
.\start.ps1
```

### Test API
```bash
python test_api.py
```

---

**Miłej nauki! 🎉**

Masz pytania? Zajrzyj do pełnej dokumentacji w `README.md`
