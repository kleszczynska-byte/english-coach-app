#!/usr/bin/env python3
"""
Test script dla English Coach API
Sprawdza czy backend działa poprawnie
"""

import requests
import json
import sys
import os

API_URL = "http://localhost:8000"

def test_root():
    """Test endpointu głównego"""
    print("🧪 Test 1: Root endpoint...")
    try:
        response = requests.get(f"{API_URL}/")
        if response.status_code == 200:
            print("✅ Root endpoint działa")
            print(f"   Odpowiedź: {response.json()}")
            return True
        else:
            print(f"❌ Błąd: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Błąd połączenia: {e}")
        return False

def test_analyze():
    """Test analizy transkrypcji"""
    print("\n🧪 Test 2: Analiza transkrypcji...")
    
    # Sprawdź klucz API
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("⚠️  Pomiń - brak ANTHROPIC_API_KEY")
        return True
    
    try:
        data = {
            "content": "During the implementation kickoff, we discussed data migration and API integration with the client's legacy system.",
            "description": "Sample implementation project"
        }
        
        response = requests.post(f"{API_URL}/analyze", json=data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Analiza działa")
            print(f"   Wydobyto {result.get('total_vocabulary_items', 0)} terminów")
            print(f"   Wydobyto {result.get('total_topics', 0)} tematów")
            return True
        else:
            print(f"❌ Błąd: Status {response.status_code}")
            print(f"   {response.text}")
            return False
    except Exception as e:
        print(f"❌ Błąd: {e}")
        return False

def test_context():
    """Test pobierania kontekstu"""
    print("\n🧪 Test 3: Pobieranie kontekstu...")
    try:
        response = requests.get(f"{API_URL}/context")
        if response.status_code == 200:
            print("✅ Kontekst działa")
            data = response.json()
            print(f"   Słownictwo: {data.get('vocabulary_count', 0)} terminów")
            print(f"   Tematy: {data.get('topics_count', 0)}")
            return True
        else:
            print(f"❌ Błąd: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Błąd: {e}")
        return False

def test_chat():
    """Test czatu"""
    print("\n🧪 Test 4: Chat endpoint...")
    
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("⚠️  Pomiń - brak ANTHROPIC_API_KEY")
        return True
    
    try:
        data = {
            "message": "Hello! Can we practice a client meeting scenario?",
            "conversation_history": []
        }
        
        response = requests.post(f"{API_URL}/chat", json=data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Chat działa")
            print(f"   Odpowiedź: {result.get('response', '')[:100]}...")
            return True
        else:
            print(f"❌ Błąd: Status {response.status_code}")
            print(f"   {response.text}")
            return False
    except Exception as e:
        print(f"❌ Błąd: {e}")
        return False

def main():
    print("=" * 60)
    print("🧪 English Coach API - Test Suite")
    print("=" * 60)
    print()
    
    # Sprawdź czy API key jest ustawiony
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("⚠️  UWAGA: ANTHROPIC_API_KEY nie jest ustawiony")
        print("   Niektóre testy zostaną pominięte")
        print()
    
    results = []
    
    # Uruchom testy
    results.append(("Root endpoint", test_root()))
    results.append(("Context", test_context()))
    
    if os.getenv("ANTHROPIC_API_KEY"):
        results.append(("Analyze", test_analyze()))
        results.append(("Chat", test_chat()))
    
    # Podsumowanie
    print("\n" + "=" * 60)
    print("📊 Podsumowanie testów")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\nWynik: {passed}/{total} testów zaliczonych")
    
    if passed == total:
        print("\n🎉 Wszystkie testy zaliczone! Backend działa poprawnie.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} testów nie powiodło się.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
