// src/app/pages/interfaces/edl.interface.ts
export type EdlType = 'IP' | 'URL' | 'DOMAIN' | 'IMEI' | 'IMSI';

export interface EDL {
    id: string;
    name: string;
    description: string;
    type: EdlType;
    createdAt: string;
    updatedAt: string;
    createdBy: string | null;
    entries: EdlEntry[];
}

export interface EdlEntry {
    id: string;
    address: string;
    comment?: string;
    type: EdlType;
    isEnabled: boolean;
    createdAt: string;
    updatedAt: string;
    createdBy: string | null;
    listName: string;
}

export interface CreateEdlListDto {
    name: string;
    description: string;
    type: EdlType;
}

export interface CreateEdlEntryDto {
    address: string;
    comment?: string;
    type: EdlType;
    listName: string;
}
