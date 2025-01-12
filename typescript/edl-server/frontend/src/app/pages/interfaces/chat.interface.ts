// frontend/src/app/shared/interfaces/chat.interface.ts

export interface ChatMessage {
    role: 'user' | 'assistant' | 'system';
    content: string;
    timestamp: Date;
}

export interface AIRSConfig {
    enabled: boolean;
    inspectRequest: boolean;
    inspectResponse: boolean;
}

export interface ChatRequestConfig {
    airs: AIRSConfig;
    chatType: 'normal' | 'stream';
    streamInspectChars: number;
}

export interface ChatRequest {
    message: string;
    config: ChatRequestConfig;
}

export interface ChatComponentConfig {
    airsEnabled: boolean;
    inspectRequest: boolean;
    inspectResponse: boolean;
    streamMode: boolean;
    streamInspectChars: number;
}

export interface ChatResponseChoice {
    message?: {
        role: string;
        content: string;
        refusal: null | string;
    };
    delta?: {
        content?: string;
    };
    index: number;
    logprobs: null;
    finish_reason: string;
}

export interface ChatResponse {
    id: string;
    object: string;
    created: number;
    model: string;
    choices: ChatResponseChoice[];
    usage: {
        prompt_tokens: number;
        completion_tokens: number;
        total_tokens: number;
    };
}

export interface StreamChunk {
    content: string;
}
