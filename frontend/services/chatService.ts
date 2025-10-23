import { API_URL, APP_AUTH_KEY } from '../api/config';
import { Persona, ChatInitResponse, ChatInvokeRequest } from '../types';


// Fetch the latest persona
export async function fetchLatestPersona(): Promise<Persona | null> {
    try {
        const response = await fetch(`${API_URL}/v1/personas/latest`, {
            headers: {
                'X-API-Key': APP_AUTH_KEY,
            },
        });
        if (!response.ok) {
            console.error('Failed to fetch persona:', response.status);
            return null;
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching persona:', error);
        return null;
    }
}

// Initialize chat session
export async function initChatSession(personaId: string): Promise<string | null> {
    try {
        const response = await fetch(`${API_URL}/v1/chat/init/${personaId}`, {
            headers: {
                'X-API-Key': APP_AUTH_KEY,
            },
        });
        if (!response.ok) {
            console.error('Failed to initialize chat session:', response.status);
            return null;
        }
        const data: ChatInitResponse = await response.json();
        return data.session_id;
    } catch (error) {
        console.error('Error initializing chat session:', error);
        return null;
    }
}

// Stream chat response
export async function* streamChatResponse(
    sessionId: string,
    message: string
): AsyncGenerator<string> {
    try {
        const requestBody: ChatInvokeRequest = {
            input_message: message,
        };

        const response = await fetch(`${API_URL}/v1/chat/stream/${sessionId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-API-Key': APP_AUTH_KEY,
            },
            body: JSON.stringify(requestBody),
        });

        if (!response.ok) {
            if (response.status === 404) {
                throw new Error('SESSION_NOT_FOUND');
            }
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const reader = response.body?.getReader();
        if (!reader) {
            throw new Error('Failed to get response reader');
        }

        const decoder = new TextDecoder();

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            const chunk = decoder.decode(value, { stream: true });
            yield chunk;
        }
    } catch (error) {
        console.error('Error streaming chat response:', error);
        throw error;
    }
}
