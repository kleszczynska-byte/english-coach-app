import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './App.css';

const API_BASE = '/api';

function App() {
  const [activeTab, setActiveTab] = useState('chat'); // 'chat', 'analyze', 'context', 'feedback'
  
  // Stan dla analizy transkrypcji
  const [transcript, setTranscript] = useState('');
  const [description, setDescription] = useState('');
  const [analysisResult, setAnalysisResult] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);
  
  // Stan dla czatu
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isSending, setIsSending] = useState(false);
  
  // Stan dla kontekstu
  const [contextData, setContextData] = useState(null);
  
  // Stan dla feedbacku
  const [feedbackData, setFeedbackData] = useState(null);
  const [loadingFeedback, setLoadingFeedback] = useState(false);
  
  const chatEndRef = useRef(null);
  
  // Auto-scroll do końca czatu
  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };
  
  useEffect(() => {
    scrollToBottom();
  }, [messages]);
  
  // Załaduj kontekst przy starcie
  useEffect(() => {
    loadContext();
  }, []);
  
  // === FUNKCJE API ===
  
  const analyzeTranscript = async () => {
    if (!transcript.trim()) {
      alert('Wprowadź transkrypcję lub opis!');
      return;
    }
    
    setAnalyzing(true);
    try {
      const response = await axios.post(`${API_BASE}/analyze`, {
        content: transcript,
        description: description || null
      });
      
      setAnalysisResult(response.data);
      setTranscript('');
      setDescription('');
      
      // Odśwież kontekst
      await loadContext();
    } catch (error) {
      console.error('Analysis error:', error);
      alert('Błąd analizy: ' + (error.response?.data?.detail || error.message));
    } finally {
      setAnalyzing(false);
    }
  };
  
  const sendMessage = async () => {
    if (!inputMessage.trim() || isSending) return;
    
    const userMessage = inputMessage.trim();
    setInputMessage('');
    
    // Dodaj wiadomość użytkownika do UI
    const newMessages = [...messages, { role: 'user', content: userMessage }];
    setMessages(newMessages);
    
    setIsSending(true);
    try {
      const response = await axios.post(`${API_BASE}/chat`, {
        message: userMessage,
        conversation_history: messages
      });
      
      // Dodaj odpowiedź asystenta
      setMessages([...newMessages, {
        role: 'assistant',
        content: response.data.response
      }]);
    } catch (error) {
      console.error('Chat error:', error);
      alert('Błąd czatu: ' + (error.response?.data?.detail || error.message));
    } finally {
      setIsSending(false);
    }
  };
  
  const loadContext = async () => {
    try {
      const response = await axios.get(`${API_BASE}/context`);
      setContextData(response.data);
    } catch (error) {
      console.error('Context load error:', error);
    }
  };
  
  const clearContext = async () => {
    if (!window.confirm('Czy na pewno chcesz wyczyścić cały kontekst i historię?')) {
      return;
    }
    
    try {
      await axios.post(`${API_BASE}/context/clear`);
      setContextData(null);
      setMessages([]);
      setAnalysisResult(null);
      setFeedbackData(null);
      await loadContext();
      alert('Kontekst wyczyszczony!');
    } catch (error) {
      console.error('Clear context error:', error);
      alert('Błąd czyszczenia kontekstu: ' + error.message);
    }
  };
  
  const loadFeedback = async () => {
    setLoadingFeedback(true);
    try {
      const response = await axios.get(`${API_BASE}/feedback`);
      setFeedbackData(response.data);
    } catch (error) {
      console.error('Feedback error:', error);
      alert('Błąd ładowania feedbacku: ' + (error.response?.data?.detail || error.message));
    } finally {
      setLoadingFeedback(false);
    }
  };
  
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };
  
  // === KOMPONENTY RENDERUJĄCE ===
  
  const renderAnalyzeTab = () => (
    <div className="tab-content">
      <h2>📝 Analiza Materiałów</h2>
      <p className="description">
        Wklej transkrypcję rozmów z klientami lub opis swoich obowiązków.
        Aplikacja wydobędzie słownictwo i <strong>automatycznie rozszerzy tematy</strong>.
      </p>
      
      <div className="form-group">
        <label>Transkrypcja / Opis rozmów:</label>
        <textarea
          value={transcript}
          onChange={(e) => setTranscript(e.target.value)}
          placeholder="Przykład: 'During the kickoff meeting, we discussed the integration roadmap with the client. They need to migrate their legacy system to our cloud platform...'"
          rows={8}
        />
      </div>
      
      <div className="form-group">
        <label>Dodatkowy opis (opcjonalnie):</label>
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Np. 'Jestem Implementation Specialist w firmie SaaS, głównie prowadzę migracje danych i integruję API...'"
          rows={4}
        />
      </div>
      
      <button 
        onClick={analyzeTranscript}
        disabled={analyzing || !transcript.trim()}
        className="btn-primary"
      >
        {analyzing ? '⏳ Analizuję...' : '🚀 Analizuj'}
      </button>
      
      {analysisResult && (
        <div className="result-box">
          <h3>✅ Analiza zakończona</h3>
          
          {analysisResult.analysis && (
            <>
              <div className="result-section">
                <h4>📚 Wydobyte słownictwo ({analysisResult.analysis.vocabulary?.length || 0}):</h4>
                <div className="tags">
                  {analysisResult.analysis.vocabulary?.map((word, idx) => (
                    <span key={idx} className="tag">{word}</span>
                  ))}
                </div>
              </div>
              
              <div className="result-section">
                <h4>🎯 Tematy rozmów ({analysisResult.analysis.topics?.length || 0}):</h4>
                <div className="tags">
                  {analysisResult.analysis.topics?.map((topic, idx) => (
                    <span key={idx} className="tag tag-topic">{topic}</span>
                  ))}
                </div>
              </div>
              
              <div className="result-section">
                <h4>➕ Rozszerzone tematy ({analysisResult.analysis.related_topics?.length || 0}):</h4>
                <div className="tags">
                  {analysisResult.analysis.related_topics?.map((topic, idx) => (
                    <span key={idx} className="tag tag-related">{topic}</span>
                  ))}
                </div>
              </div>
              
              <div className="result-section">
                <h4>💡 Sugerowane słownictwo ({analysisResult.analysis.suggested_vocabulary?.length || 0}):</h4>
                <div className="tags">
                  {analysisResult.analysis.suggested_vocabulary?.map((word, idx) => (
                    <span key={idx} className="tag tag-suggested">{word}</span>
                  ))}
                </div>
              </div>
              
              <div className="result-section">
                <h4>📊 Poziom językowy:</h4>
                <p>{analysisResult.analysis.language_level}</p>
              </div>
              
              <div className="result-section">
                <h4>📝 Podsumowanie:</h4>
                <p>{analysisResult.analysis.summary}</p>
              </div>
            </>
          )}
          
          <p className="meta">
            📦 W bazie: {analysisResult.total_vocabulary_items} terminów, 
            {analysisResult.total_topics} tematów
          </p>
        </div>
      )}
    </div>
  );
  
  const renderChatTab = () => (
    <div className="tab-content chat-tab">
      <h2>💬 Rozmowa z Coachem</h2>
      <p className="description">
        Ćwicz angielski B2 w kontekście swojej pracy. Coach będzie korygował błędy i rozwijał tematy.
      </p>
      
      <div className="chat-container">
        <div className="messages">
          {messages.length === 0 && (
            <div className="welcome-message">
              <h3>👋 Witaj!</h3>
              <p>Zacznij rozmowę po angielsku. Mogę z Tobą porozmawiać o:</p>
              <ul>
                <li>🚀 Projektach wdrożeniowych (implementations, deployments)</li>
                <li>💼 Komunikacji z klientem (stakeholder management)</li>
                <li>🔧 Problemach technicznych (troubleshooting)</li>
                <li>📊 Raportowaniu statusu (status updates, reporting)</li>
                <li>🤝 Spotkaniach zespołowych (standups, retrospectives)</li>
              </ul>
              <p><strong>Przykład:</strong> "Hi! Yesterday we had a kickoff meeting with a new client..."</p>
            </div>
          )}
          
          {messages.map((msg, idx) => (
            <div key={idx} className={`message ${msg.role}`}>
              <div className="message-header">
                {msg.role === 'user' ? '👤 Ty' : '🤖 Coach'}
              </div>
              <div className="message-content">
                {msg.content.split('\n').map((line, lineIdx) => (
                  <p key={lineIdx}>{line}</p>
                ))}
              </div>
            </div>
          ))}
          
          {isSending && (
            <div className="message assistant">
              <div className="message-header">🤖 Coach</div>
              <div className="message-content typing">
                <span></span><span></span><span></span>
              </div>
            </div>
          )}
          
          <div ref={chatEndRef} />
        </div>
        
        <div className="chat-input-container">
          <textarea
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message in English... (Press Enter to send, Shift+Enter for new line)"
            rows={3}
            disabled={isSending}
          />
          <button 
            onClick={sendMessage}
            disabled={isSending || !inputMessage.trim()}
            className="btn-send"
          >
            {isSending ? '⏳' : '📤'} Send
          </button>
        </div>
      </div>
    </div>
  );
  
  const renderContextTab = () => (
    <div className="tab-content">
      <h2>🧠 Twój Kontekst</h2>
      <p className="description">
        Przegląd słownictwa i tematów, które aplikacja rozpoznała z Twoich materiałów.
      </p>
      
      <button onClick={loadContext} className="btn-secondary">
        🔄 Odśwież
      </button>
      
      <button onClick={clearContext} className="btn-danger" style={{marginLeft: '10px'}}>
        🗑️ Wyczyść wszystko
      </button>
      
      {contextData && (
        <div className="context-display">
          <div className="stat-box">
            <div className="stat-number">{contextData.vocabulary_count}</div>
            <div className="stat-label">Terminów w bazie</div>
          </div>
          
          <div className="stat-box">
            <div className="stat-number">{contextData.topics_count}</div>
            <div className="stat-label">Tematów</div>
          </div>
          
          <div className="stat-box">
            <div className="stat-number">{contextData.transcripts_count}</div>
            <div className="stat-label">Przeanalizowanych materiałów</div>
          </div>
          
          <div className="stat-box">
            <div className="stat-number">{contextData.conversations_count}</div>
            <div className="stat-label">Rozmów z coachem</div>
          </div>
          
          <div className="result-section">
            <h4>📚 Słownictwo (pierwsze 50):</h4>
            <div className="tags">
              {contextData.vocabulary?.map((word, idx) => (
                <span key={idx} className="tag">{word}</span>
              ))}
            </div>
          </div>
          
          <div className="result-section">
            <h4>🎯 Tematy (pierwsze 20):</h4>
            <div className="tags">
              {contextData.topics?.map((topic, idx) => (
                <span key={idx} className="tag tag-topic">{topic}</span>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
  
  const renderFeedbackTab = () => (
    <div className="tab-content">
      <h2>📊 Twoje Postępy</h2>
      <p className="description">
        Analiza Twoich rozmów z coachem - mocne strony i obszary do poprawy.
      </p>
      
      <button 
        onClick={loadFeedback}
        disabled={loadingFeedback}
        className="btn-primary"
      >
        {loadingFeedback ? '⏳ Generuję raport...' : '📈 Generuj raport'}
      </button>
      
      {feedbackData && feedbackData.status === 'no_data' && (
        <div className="info-box">
          <p>{feedbackData.message}</p>
          <p>Rozpocznij rozmowy w zakładce "Rozmowa", a potem wróć tutaj!</p>
        </div>
      )}
      
      {feedbackData && feedbackData.feedback && (
        <div className="feedback-display">
          <p className="meta">
            Przeanalizowano: {feedbackData.analyzed_conversations} ostatnich rozmów
          </p>
          
          <div className="feedback-section success">
            <h3>💪 Mocne strony</h3>
            <ul>
              {feedbackData.feedback.strengths?.map((strength, idx) => (
                <li key={idx}>{strength}</li>
              ))}
            </ul>
          </div>
          
          <div className="feedback-section warning">
            <h3>🎯 Obszary do poprawy</h3>
            <ul>
              {feedbackData.feedback.areas_for_improvement?.map((area, idx) => (
                <li key={idx}>{area}</li>
              ))}
            </ul>
          </div>
          
          <div className="feedback-section info">
            <h3>💡 Rekomendacje</h3>
            <ul>
              {feedbackData.feedback.recommendations?.map((rec, idx) => (
                <li key={idx}>{rec}</li>
              ))}
            </ul>
          </div>
          
          <div className="feedback-section">
            <h3>📈 Notatki o postępach</h3>
            <p>{feedbackData.feedback.progress_notes}</p>
          </div>
        </div>
      )}
    </div>
  );
  
  // === GŁÓWNY RENDER ===
  
  return (
    <div className="app">
      <header className="header">
        <h1>🎓 English Coach B2</h1>
        <p>Dla Implementation Specialists</p>
      </header>
      
      <div className="tabs">
        <button 
          className={activeTab === 'chat' ? 'active' : ''}
          onClick={() => setActiveTab('chat')}
        >
          💬 Rozmowa
        </button>
        <button 
          className={activeTab === 'analyze' ? 'active' : ''}
          onClick={() => setActiveTab('analyze')}
        >
          📝 Analiza
        </button>
        <button 
          className={activeTab === 'context' ? 'active' : ''}
          onClick={() => setActiveTab('context')}
        >
          🧠 Kontekst
        </button>
        <button 
          className={activeTab === 'feedback' ? 'active' : ''}
          onClick={() => setActiveTab('feedback')}
        >
          📊 Postępy
        </button>
      </div>
      
      <main className="main-content">
        {activeTab === 'chat' && renderChatTab()}
        {activeTab === 'analyze' && renderAnalyzeTab()}
        {activeTab === 'context' && renderContextTab()}
        {activeTab === 'feedback' && renderFeedbackTab()}
      </main>
      
      <footer className="footer">
        <p>Powered by Claude API • {new Date().getFullYear()}</p>
      </footer>
    </div>
  );
}

export default App;
