import React, { useState, useEffect, useCallback, useRef } from 'react';
import { Header } from './components/Header';
import { ChatLog } from './components/ChatLog';
import { MessageInput } from './components/MessageInput';
import { Message, Persona } from './types';
import { fetchLatestPersona, initChatSession, streamChatResponse } from './services/chatService';

const App: React.FC = () => {
    const [messages, setMessages] = useState<Message[]>([]);
    const [streamingMessage, setStreamingMessage] = useState<string>('');
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [persona, setPersona] = useState<Persona | null>(null);
    const [sessionId, setSessionId] = useState<string | null>(null);
    const [isOnline, setIsOnline] = useState<boolean>(false);

    const sessionIdRef = useRef<string | null>(null);

    // Update document title and favicon when persona is loaded
    useEffect(() => {
        if (persona) {
            document.title = `${persona.public_name} - Ask Me Anything`;

            if (persona.profile_image_url) {
                let favicon = document.querySelector("link[rel*='icon']") as HTMLLinkElement;
                if (!favicon) {
                    favicon = document.createElement('link');
                    favicon.rel = 'icon';
                    document.head.appendChild(favicon);
                }
                favicon.href = persona.profile_image_url;
            }
        }
    }, [persona]);

    // Fetch persona and initialize session on mount
    useEffect(() => {
        const initializeApp = async () => {
            // Fetch persona
            const fetchedPersona = await fetchLatestPersona();
            if (fetchedPersona) {
                setPersona(fetchedPersona);
                setIsOnline(true);

                // Initialize chat session
                const newSessionId = await initChatSession(fetchedPersona.id);
                if (newSessionId) {
                    setSessionId(newSessionId);
                    sessionIdRef.current = newSessionId;

                    // Add welcome message if available
                    if (fetchedPersona.welcome_message) {
                        setMessages([
                            {
                                id: '1',
                                text: fetchedPersona.welcome_message,
                                sender: 'bot',
                            },
                        ]);
                    }
                } else {
                    setIsOnline(false);
                }
            } else {
                setIsOnline(false);
            }
        };

        initializeApp();
    }, []);

    // Reinitialize session
    const reinitializeSession = useCallback(async () => {
        if (!persona) return null;

        const newSessionId = await initChatSession(persona.id);
        if (newSessionId) {
            setSessionId(newSessionId);
            sessionIdRef.current = newSessionId;
            return newSessionId;
        }
        return null;
    }, [persona]);

    const handleSendMessage = useCallback(async (text: string) => {
        if (!text.trim() || !sessionId || !persona) return;

        const userMessage: Message = { id: Date.now().toString(), text, sender: 'user' };
        setMessages(prev => [...prev, userMessage]);
        setIsLoading(true);
        setStreamingMessage('');

        let accumulatedText = '';
        let currentSessionId = sessionIdRef.current;

        try {
            if (!currentSessionId) {
                throw new Error('No session ID available');
            }

            const stream = streamChatResponse(currentSessionId, text);
            for await (const chunk of stream) {
                accumulatedText += chunk;
                setStreamingMessage(accumulatedText);
            }
        } catch (error: any) {
            console.error("Error streaming response:", error);

            // Handle session not found error
            if (error.message === 'SESSION_NOT_FOUND') {
                console.log('Session not found, reinitializing...');

                // Clear chat history
                setMessages([]);
                setStreamingMessage('');

                // Reinitialize session
                const newSessionId = await reinitializeSession();

                if (newSessionId) {
                    // Add welcome message back if available
                    if (persona.welcome_message) {
                        setMessages([
                            {
                                id: '1',
                                text: persona.welcome_message,
                                sender: 'bot',
                            },
                        ]);
                    }

                    // Inform user about session reset
                    accumulatedText = "Sorry, the session was reset. Please try sending your message again.";
                } else {
                    accumulatedText = "Sorry, I couldn't establish a connection. Please refresh the page.";
                    setIsOnline(false);
                }
            } else {
                accumulatedText = "Sorry, I encountered an error.";
            }
        } finally {
            if (accumulatedText) {
                setMessages(prev => [...prev, { id: (Date.now() + 1).toString(), text: accumulatedText, sender: 'bot' }]);
            }
            setStreamingMessage('');
            setIsLoading(false);
        }
    }, [sessionId, persona, reinitializeSession]);

    return (
        <div className="bg-[#07080A] text-white font-jetbrains-mono min-h-screen flex flex-col items-center">
            <div className="w-full max-w-3xl h-screen flex flex-col p-4 sm:p-6 md:p-8">
                <Header persona={persona} isOnline={isOnline} />
                <ChatLog messages={messages} streamingMessage={streamingMessage} isLoading={isLoading} />
                <MessageInput onSendMessage={handleSendMessage} disabled={isLoading || !isOnline} />
            </div>
        </div>
    );
};

export default App;
