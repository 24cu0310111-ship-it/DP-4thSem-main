import { useState, useRef, useEffect } from 'react';
import type { ChatMessage } from '../types';
import api from '../services/api';

const INITIAL_MESSAGES: ChatMessage[] = [
  {
    id: '1',
    role: 'ai',
    content: 'Hello! I\'m the SCMS AI assistant. I can help you file a complaint quickly.\n\nPlease describe your issue — you can type, upload a photo, or record a voice message.',
    timestamp: new Date().toISOString(),
  },
];

export default function AIChatIntake() {
  const [messages, setMessages] = useState<ChatMessage[]>(INITIAL_MESSAGES);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [lastAnalysis, setLastAnalysis] = useState<ChatMessage['metadata'] | null>(null);
  const [detectedLocation, setDetectedLocation] = useState<string>('');
  const [isLocating, setIsLocating] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async (userMsg: string) => {
    setIsTyping(true);
    try {
      const { data } = await api.post('/user/chat', {
        message: userMsg,
        session_id: sessionId,
      });

      // Store session ID for continuing the conversation
      if (data.session_id) {
        setSessionId(data.session_id);
      }

      const metadata: ChatMessage['metadata'] = data.metadata
        ? {
            detected_category: data.metadata.detected_category,
            detected_priority: data.metadata.detected_priority,
            confidence: data.metadata.confidence,
          }
        : undefined;

      if (data.metadata) {
        setLastAnalysis(metadata);
      }

      setMessages((prev) => [
        ...prev,
        {
          id: String(Date.now()),
          role: 'ai',
          content: data.content,
          timestamp: data.timestamp || new Date().toISOString(),
          metadata,
        },
      ]);
    } catch (err) {
      console.error('Chat API error:', err);
      // Fallback to a generic error message
      setMessages((prev) => [
        ...prev,
        {
          id: String(Date.now()),
          role: 'ai',
          content: 'I\'m having trouble connecting right now. Please try again in a moment.',
          timestamp: new Date().toISOString(),
        },
      ]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleFileComplaint = async () => {
    if (!sessionId) return;
    setIsTyping(true);
    try {
      const { data } = await api.post('/user/chat/file-complaint', {
        session_id: sessionId,
        category: lastAnalysis?.detected_category || undefined,
        location: detectedLocation || '', // Use exact GPS coordinates if available
      });

      setMessages((prev) => [
        ...prev,
        {
          id: String(Date.now()),
          role: 'ai',
          content: `✅ **Complaint filed successfully!**\n\nYour complaint ID is **${data.complaint_id}**. Priority: **${data.priority_level}**.\n\n${data.message}\n\nYou can track its progress in your complaint history.`,
          timestamp: new Date().toISOString(),
        },
      ]);
      // Reset session for a new conversation
      setSessionId(null);
      setLastAnalysis(null);
    } catch (err) {
      console.error('File complaint error:', err);
      setMessages((prev) => [
        ...prev,
        {
          id: String(Date.now()),
          role: 'ai',
          content: 'Sorry, I couldn\'t file the complaint right now. Please try again.',
          timestamp: new Date().toISOString(),
        },
      ]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleDetectLocation = () => {
    if (!navigator.geolocation) {
      alert("Geolocation is not supported by your browser");
      return;
    }
    setIsLocating(true);
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const { latitude, longitude } = pos.coords;
        const coordsStr = `${latitude.toFixed(5)}, ${longitude.toFixed(5)}`;
        setDetectedLocation(coordsStr);
        setIsLocating(false);
        setMessages((prev) => [
          ...prev,
          {
            id: String(Date.now()),
            role: 'user',
            content: `📍 Location pinned: ${coordsStr}`,
            timestamp: new Date().toISOString(),
          },
        ]);
      },
      (err) => {
        console.error('Location error:', err);
        setIsLocating(false);
        alert("Failed to get location. Please ensure location services are enabled.");
      }
    );
  };

  const handleSend = () => {
    if (!input.trim()) return;
    const userMessage: ChatMessage = {
      id: String(Date.now()),
      role: 'user',
      content: input,
      timestamp: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, userMessage]);
    const msg = input;
    setInput('');

    // Check if user is confirming to file
    const lower = msg.toLowerCase();
    if (
      sessionId &&
      lastAnalysis?.detected_category &&
      (lower.includes('yes') || lower.includes('file') || lower.includes('proceed') || lower.includes('confirm'))
    ) {
      handleFileComplaint();
    } else {
      sendMessage(msg);
    }
  };

  return (
    <div className="flex flex-col lg:flex-row h-[calc(100vh-4rem)] md:h-screen">
      {/* Chat area */}
      <div className="flex-1 flex flex-col">
        {/* Chat header */}
        <div className="px-6 py-4 border-b border-outline-variant/10 bg-surface-container-low">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-tertiary-container/20 flex items-center justify-center intelligence-glow">
              <span className="material-symbols-outlined text-tertiary">smart_toy</span>
            </div>
            <div>
              <h2 className="text-base font-headline font-semibold text-on-surface">AI Complaint Assistant</h2>
              <p className="text-xs text-tertiary flex items-center gap-1">
                <span className="w-1.5 h-1.5 rounded-full bg-tertiary-container animate-pulse" />
                Online — Ready to help
              </p>
            </div>
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages.map((msg) => (
            <div key={msg.id} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-[80%] lg:max-w-[60%] rounded-obsidian p-4 ${
                msg.role === 'user'
                  ? 'bg-primary-container/20 text-on-surface ml-12'
                  : 'bg-surface-container ghost-border mr-12'
              }`}>
                <p className="text-sm font-body whitespace-pre-wrap leading-relaxed">{msg.content}</p>
                {msg.metadata && (
                  <div className="mt-3 pt-3 border-t border-outline-variant/10 flex flex-wrap gap-2">
                    {msg.metadata.detected_category && (
                      <span className="chip-active inline-flex items-center px-2.5 py-1 rounded-full bg-secondary-container/30 text-on-secondary-container text-xs font-label">
                        {msg.metadata.detected_category}
                      </span>
                    )}
                    {msg.metadata.detected_priority && (
                      <span className="inline-flex items-center px-2.5 py-1 rounded-full bg-tertiary-container/20 text-tertiary text-xs font-label uppercase">
                        {msg.metadata.detected_priority}
                      </span>
                    )}
                    {msg.metadata.confidence && (
                      <span className="text-xs text-on-surface-variant">
                        {Math.round(msg.metadata.confidence * 100)}% confidence
                      </span>
                    )}
                  </div>
                )}
                <p className="text-[10px] text-outline mt-2">{new Date(msg.timestamp).toLocaleTimeString()}</p>
              </div>
            </div>
          ))}

          {isTyping && (
            <div className="flex justify-start">
              <div className="bg-surface-container ghost-border rounded-obsidian p-4 mr-12">
                <div className="flex gap-1.5">
                  <span className="w-2 h-2 rounded-full bg-tertiary-container animate-bounce [animation-delay:0ms]" />
                  <span className="w-2 h-2 rounded-full bg-tertiary-container animate-bounce [animation-delay:150ms]" />
                  <span className="w-2 h-2 rounded-full bg-tertiary-container animate-bounce [animation-delay:300ms]" />
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <div className="px-6 py-4 border-t border-outline-variant/10 bg-surface-container-low">
          <div className="flex items-center gap-2">
            <button className="p-2 text-on-surface-variant hover:text-on-surface hover:bg-surface-container rounded-obsidian transition-all" title="Attach file">
              <span className="material-symbols-outlined">attach_file</span>
            </button>
            <button className="p-2 text-on-surface-variant hover:text-on-surface hover:bg-surface-container rounded-obsidian transition-all" title="Voice input">
              <span className="material-symbols-outlined">mic</span>
            </button>
            <button 
              onClick={handleDetectLocation}
              disabled={isLocating}
              className={`p-2 rounded-obsidian transition-all ${detectedLocation ? 'bg-primary-container/10 text-primary-container' : 'text-on-surface-variant hover:text-on-surface hover:bg-surface-container'} ${isLocating ? 'animate-pulse' : ''}`} 
              title="Detect Precise Location"
            >
              <span className="material-symbols-outlined">
                {detectedLocation ? 'location_on' : 'my_location'}
              </span>
            </button>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
              placeholder="Describe your issue..."
              className="flex-1 input-obsidian px-4 py-3 rounded-obsidian text-sm"
            />
            <button
              onClick={handleSend}
              disabled={!input.trim()}
              className="p-2.5 rounded-obsidian gradient-primary text-on-primary transition-all hover:scale-105 disabled:opacity-40 disabled:hover:scale-100"
            >
              <span className="material-symbols-outlined">send</span>
            </button>
          </div>
        </div>
      </div>

      {/* AI Summary sidebar — desktop only */}
      <div className="hidden lg:block w-80 border-l border-outline-variant/10 bg-surface-container-low p-6 overflow-y-auto">
        <h3 className="label-caps text-tertiary mb-4">AI Analysis</h3>
        <div className="space-y-4">
          <div className="bg-surface-container rounded-obsidian p-4 ghost-border">
            <p className="label-caps text-on-surface-variant mb-2">Detected Category</p>
            <p className="text-on-surface font-body text-sm">
              {messages.findLast((m) => m.metadata?.detected_category)?.metadata?.detected_category || '—'}
            </p>
          </div>
          <div className="bg-surface-container rounded-obsidian p-4 ghost-border">
            <p className="label-caps text-on-surface-variant mb-2">Priority Level</p>
            <p className="text-on-surface font-body text-sm capitalize">
              {messages.findLast((m) => m.metadata?.detected_priority)?.metadata?.detected_priority || '—'}
            </p>
          </div>
          <div className="bg-surface-container rounded-obsidian p-4 ghost-border">
            <p className="label-caps text-on-surface-variant mb-2">Confidence</p>
            <div className="flex items-center gap-2">
              <div className="flex-1 h-2 bg-surface-container-high rounded-full overflow-hidden">
                <div
                  className="h-full bg-tertiary-container rounded-full transition-all duration-500"
                  style={{ width: `${(messages.findLast((m) => m.metadata?.confidence)?.metadata?.confidence || 0) * 100}%` }}
                />
              </div>
              <span className="text-sm text-on-surface">
                {Math.round((messages.findLast((m) => m.metadata?.confidence)?.metadata?.confidence || 0) * 100)}%
              </span>
            </div>
          </div>

          {/* File Complaint button — appears when we have analysis */}
          {lastAnalysis?.detected_category && (
            <button
              onClick={handleFileComplaint}
              disabled={isTyping}
              className="w-full py-3 rounded-obsidian gradient-primary text-on-primary font-label text-sm transition-all hover:scale-[1.02] disabled:opacity-40"
            >
              <span className="material-symbols-outlined text-sm align-middle mr-1">description</span>
              File Complaint
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

