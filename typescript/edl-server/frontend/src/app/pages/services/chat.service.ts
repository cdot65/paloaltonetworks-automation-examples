// frontend/src/app/shared/services/chat.service.ts
import { Injectable } from '@angular/core';
import { environmentProd } from '../../../environments/environment';
import { Subject, BehaviorSubject } from 'rxjs';
import {
    ChatMessage,
    ChatRequest,
    ChatResponse,
    StreamChunk,
} from '../interfaces/chat.interface';

@Injectable({
    providedIn: 'root',
})
export class ChatService {
    private messageSubject = new Subject<ChatMessage>();
    messages$ = this.messageSubject.asObservable();
    private errorSubject = new BehaviorSubject<string | null>(null);

    async sendMessageStream(request: ChatRequest): Promise<void> {
        const assistantMessage: ChatMessage = {
            role: 'assistant',
            content: '',
            timestamp: new Date(),
        };

        const response = await fetch(`${environmentProd.apiUrl}/chat/stream`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(request),
        });

        if (!response.ok) {
            this.handleError(`HTTP error: ${response.status}`);
            return;
        }

        const reader = response.body?.getReader();
        if (!reader) {
            this.handleError('Response body is not readable');
            return;
        }

        const decoder = new TextDecoder();

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            const chunk = decoder.decode(value);
            const lines = chunk.split('\n');

            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    const parsedData = this.parseStreamData(line.slice(6));
                    if (!parsedData) continue;

                    assistantMessage.content += parsedData.content;
                    this.messageSubject.next({ ...assistantMessage });
                }
            }
        }
    }

    async sendMessageNormal(request: ChatRequest): Promise<void> {
        const response = await fetch(`${environmentProd.apiUrl}/chat/normal`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(request),
        });

        if (!response.ok) {
            this.handleError(`HTTP error: ${response.status}`);
            return;
        }

        const data = (await response.json()) as ChatResponse;

        // Check for message content first, then delta content as fallback
        const content =
            data.choices[0]?.message?.content ??
            data.choices[0]?.delta?.content ??
            'No content received';

        this.addMessage({
            role: 'assistant',
            content,
            timestamp: new Date(),
        });
    }

    private addMessage(message: ChatMessage): void {
        this.messageSubject.next(message);
    }

    private handleError(message: string): void {
        const errorMessage: ChatMessage = {
            role: 'system',
            content: `Error: ${message}`,
            timestamp: new Date(),
        };
        this.addMessage(errorMessage);
        this.errorSubject.next(message);
    }

    private parseStreamData(data: string): StreamChunk | null {
        try {
            return JSON.parse(data) as StreamChunk;
        } catch {
            this.handleError('Error parsing stream data');
            return null;
        }
    }
}
