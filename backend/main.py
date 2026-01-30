from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import anthropic
import json
import os
from datetime import datetime

app = FastAPI(title="English Coach API")

# CORS dla frontendu
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modele danych
class TranscriptInput(BaseModel):
    content: str
    description: Optional[str] = None

class ConversationMessage(BaseModel):
    role: str  # "user" lub "assistant"
    content: str

class ChatRequest(BaseModel):
    message: str
    conversation_history: List[ConversationMessage] = []

class VocabularyContext(BaseModel):
    transcripts: List[str] = []
    descriptions: List[str] = []

# Globalna baza kontekstu użytkownika
user_context = {
    "vocabulary": [],
    "topics": [],
    "transcripts": [],
    "descriptions": [],
    "conversation_history": []
}

@app.get("/")
async def root():
    return {
        "message": "English Coach API is running",
        "version": "1.0.0",
        "endpoints": ["/analyze", "/chat", "/context", "/feedback"]
    }

@app.post("/analyze")
async def analyze_transcript(data: TranscriptInput):
    """
    Analizuje transkrypcję lub opis, aby wydobyć słownictwo i tematy.
    Nie ogranicza się tylko do podanych słów - rozszerza kontekst.
    """
    try:
        # Tutaj będzie API key użytkownika (w produkcji z .env)
        api_key = os.getenv("ANTHROPIC_API_KEY", "")
        
        if not api_key:
            raise HTTPException(
                status_code=500, 
                detail="ANTHROPIC_API_KEY not configured. Add it to environment variables."
            )
        
        client = anthropic.Anthropic(api_key=api_key)
        
        # Prompt dla Claude do analizy kontekstu
        analysis_prompt = f"""Przeanalizuj poniższą transkrypcję/opis z pracy wdrożeniowca IT.

Twoje zadanie:
1. Wyodrębnij kluczowe słownictwo branżowe (techniczne i biznesowe)
2. Zidentyfikuj główne tematy rozmów
3. **WAŻNE**: Rozszerz kontekst - zaproponuj powiązane tematy i słownictwo, które wdrożeniowiec powinien znać, nawet jeśli nie pojawiło się w transkrypcji
4. Oceń poziom językowy materiału wejściowego

Transkrypcja/Opis:
{data.content}

Zwróć odpowiedź w formacie JSON:
{{
    "vocabulary": ["lista", "słów", "kluczowych"],
    "topics": ["główne", "tematy"],
    "related_topics": ["powiązane", "tematy", "do", "nauki"],
    "suggested_vocabulary": ["dodatkowe", "słowa", "przydatne", "w", "tej", "dziedzinie"],
    "language_level": "ocena poziomu językowego tekstu",
    "summary": "krótkie podsumowanie kontekstu pracy"
}}"""
        
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{
                "role": "user",
                "content": analysis_prompt
            }]
        )
        
        # Parsowanie odpowiedzi Claude
        response_text = message.content[0].text
        
        # Wyciągnij JSON z odpowiedzi (Claude może dodać tekst przed/po JSON)
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1
        
        if start_idx != -1 and end_idx != 0:
            json_str = response_text[start_idx:end_idx]
            analysis = json.loads(json_str)
        else:
            # Fallback jeśli nie ma JSON
            analysis = {
                "vocabulary": [],
                "topics": [],
                "related_topics": [],
                "suggested_vocabulary": [],
                "language_level": "Unknown",
                "summary": response_text
            }
        
        # Zapisz do kontekstu
        user_context["transcripts"].append(data.content)
        if data.description:
            user_context["descriptions"].append(data.description)
        
        # Aktualizuj słownictwo i tematy (unikalne wartości)
        user_context["vocabulary"] = list(set(
            user_context["vocabulary"] + 
            analysis.get("vocabulary", []) + 
            analysis.get("suggested_vocabulary", [])
        ))
        user_context["topics"] = list(set(
            user_context["topics"] + 
            analysis.get("topics", []) + 
            analysis.get("related_topics", [])
        ))
        
        return {
            "status": "success",
            "analysis": analysis,
            "context_updated": True,
            "total_vocabulary_items": len(user_context["vocabulary"]),
            "total_topics": len(user_context["topics"])
        }
        
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"Error parsing Claude response: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")

@app.post("/chat")
async def chat_with_coach(request: ChatRequest):
    """
    Prowadzi rozmowę z użytkownikiem w kontekście jego pracy.
    - Używa zgromadzonego kontekstu
    - Koryguje błędy
    - Rozszerza tematykę poza podane przykłady
    """
    try:
        api_key = os.getenv("ANTHROPIC_API_KEY", "")
        
        if not api_key:
            raise HTTPException(
                status_code=500,
                detail="ANTHROPIC_API_KEY not configured"
            )
        
        client = anthropic.Anthropic(api_key=api_key)
        
        # Buduj system prompt z kontekstem użytkownika
        vocabulary_context = ", ".join(user_context["vocabulary"][:50]) if user_context["vocabulary"] else "brak jeszcze"
        topics_context = ", ".join(user_context["topics"][:20]) if user_context["topics"] else "brak jeszcze"
        
        system_prompt = f"""Jesteś ekspertem od nauczania angielskiego biznesowego na poziomie B2, specjalizującym się w pracy wdrożeniowca IT.

KONTEKST UŻYTKOWNIKA:
- Słownictwo z pracy: {vocabulary_context}
- Tematy rozmów: {topics_context}

TWOJE ZADANIA:
1. **Prowadź naturalną konwersację** w kontekście pracy wdrożeniowca (implementacje, integracje, projekty IT, komunikacja z klientem)
2. **Rozszerzaj tematykę** - nie ograniczaj się tylko do podanych słów, wprowadzaj nowe tematy związane z wdrożeniami
3. **Koryguj błędy** - po każdej wypowiedzi użytkownika:
   - Jeśli są błędy gramatyczne, leksykalne lub stylistyczne - wskaż je delikatnie
   - Zaproponuj lepsze sformułowanie
   - Wyjaśnij dlaczego to lepsze
4. **Dostosuj poziom B2** - używaj przysłownego czasu przeszłego, trybu warunkowego, strony biernej
5. **Bądź konwersacyjny** - zadawaj pytania, symuluj prawdziwe sytuacje z pracy

FORMAT ODPOWIEDZI:
Gdy użytkownik pisze z błędami, odpowiedz tak:

[KOREKTA]
❌ "I will implemented the feature yesterday"
✅ "I implemented the feature yesterday" 
💡 Używamy Past Simple (implemented), nie Future + Past Participle

[ROZMOWA]
That's great that you completed it! How did the client react to the new feature? Did you encounter any integration challenges?

Jeśli użytkownik pisze bezbłędnie, pomiń sekcję [KOREKTA] i prowadź rozmowę normalnie.

WAŻNE:
- Rozmawiaj PO ANGIELSKU
- Korekty mogą być po polsku (dla lepszego zrozumienia) lub po angielsku
- Wprowadzaj nowe scenariusze: daily standup, client demo, technical discussion, problem solving
- Używaj słownictwa z jego pracy, ale też wprowadzaj nowe terminy"""

        # Zbuduj historię konwersacji
        messages = []
        for msg in request.conversation_history[-10:]:  # Ostatnie 10 wiadomości
            messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        # Dodaj nową wiadomość użytkownika
        messages.append({
            "role": "user",
            "content": request.message
        })
        
        # Wywołaj Claude
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            system=system_prompt,
            messages=messages
        )
        
        assistant_response = response.content[0].text
        
        # Zapisz do historii
        user_context["conversation_history"].append({
            "timestamp": datetime.now().isoformat(),
            "user": request.message,
            "assistant": assistant_response
        })
        
        return {
            "status": "success",
            "response": assistant_response,
            "conversation_length": len(user_context["conversation_history"])
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")

@app.get("/context")
async def get_context():
    """Zwraca obecny kontekst użytkownika"""
    return {
        "vocabulary_count": len(user_context["vocabulary"]),
        "topics_count": len(user_context["topics"]),
        "transcripts_count": len(user_context["transcripts"]),
        "conversations_count": len(user_context["conversation_history"]),
        "vocabulary": user_context["vocabulary"][:50],  # Pierwsze 50
        "topics": user_context["topics"][:20]  # Pierwsze 20
    }

@app.post("/context/clear")
async def clear_context():
    """Czyści kontekst użytkownika"""
    user_context["vocabulary"] = []
    user_context["topics"] = []
    user_context["transcripts"] = []
    user_context["descriptions"] = []
    user_context["conversation_history"] = []
    return {"status": "success", "message": "Context cleared"}

@app.get("/feedback")
async def get_feedback_summary():
    """Generuje podsumowanie postępów użytkownika"""
    try:
        if not user_context["conversation_history"]:
            return {
                "status": "no_data",
                "message": "Brak jeszcze konwersacji do analizy"
            }
        
        api_key = os.getenv("ANTHROPIC_API_KEY", "")
        if not api_key:
            raise HTTPException(status_code=500, detail="ANTHROPIC_API_KEY not configured")
        
        client = anthropic.Anthropic(api_key=api_key)
        
        # Zbierz ostatnie 20 wymian
        recent_conversations = user_context["conversation_history"][-20:]
        conversation_text = "\n\n".join([
            f"User: {conv['user']}\nAssistant: {conv['assistant']}"
            for conv in recent_conversations
        ])
        
        feedback_prompt = f"""Przeanalizuj poniższe konwersacje użytkownika uczącego się angielskiego na poziomie B2 w kontekście pracy wdrożeniowca.

{conversation_text}

Dostarcz zwięzłe podsumowanie:
1. **Mocne strony** - co użytkownik robi dobrze
2. **Obszary do poprawy** - najczęstsze błędy i słabości
3. **Rekomendacje** - konkretne ćwiczenia i tematy do praktyki
4. **Postępy** - czy widać rozwój w trakcie rozmów

Odpowiedz w formacie JSON:
{{
    "strengths": ["mocna", "strona", "1", ...],
    "areas_for_improvement": ["obszar", "1", ...],
    "recommendations": ["rekomendacja", "1", ...],
    "progress_notes": "opis postępów"
}}"""
        
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1500,
            messages=[{"role": "user", "content": feedback_prompt}]
        )
        
        response_text = response.content[0].text
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1
        
        if start_idx != -1 and end_idx != 0:
            feedback = json.loads(response_text[start_idx:end_idx])
        else:
            feedback = {
                "strengths": [],
                "areas_for_improvement": [],
                "recommendations": [],
                "progress_notes": response_text
            }
        
        return {
            "status": "success",
            "feedback": feedback,
            "analyzed_conversations": len(recent_conversations)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Feedback error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
