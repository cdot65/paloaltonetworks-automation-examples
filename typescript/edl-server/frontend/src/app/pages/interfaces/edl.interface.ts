// src/app/pages/interfaces/edl.interface.ts
export interface EDLEntry {
    id: string;
    address: string;
    comment: string;
    type: 'IP' | 'URL' | 'DOMAIN';
    isEnabled: boolean;
    createdAt: string;
    updatedAt: string;
    createdBy: string | null;
    listName: string;
}

export interface EDL {
    id: string;
    name: string;
    description: string;
    type: 'IP' | 'URL' | 'DOMAIN';
    createdAt: string;
    updatedAt: string;
    createdBy: string | null;
    entries: EDLEntry[];
}

export interface CreateEdlListDto {
    name: string;
    description: string;
    type: 'IP' | 'URL' | 'DOMAIN';
}

export interface CreateEdlEntryDto {
    address: string;
    comment?: string;
    listName: string;
}

// View model for the table display
export interface EDLViewModel {
    id: string;
    name: string;
    description: string;
    type: 'IP' | 'URL' | 'DOMAIN';
    entryCount: number;
    lastUpdated: string;
}
