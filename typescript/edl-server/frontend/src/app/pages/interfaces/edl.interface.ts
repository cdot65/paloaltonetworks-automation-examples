// src/app/pages/interfaces/edl.interface.ts

// Define types (matching backend)
export enum EntryType {
    IP = 'IP',
    URL = 'URL',
    DOMAIN = 'DOMAIN',
    IMEI = 'IMEI',
    IMSI = 'IMSI'
}

export enum ListType {
    IP = 'IP',
    URL = 'URL',
    DOMAIN = 'DOMAIN',
    EQUIPMENT_IDENTITY = 'EQUIPMENT_IDENTITY',
    SUBSCRIBER_IDENTITY = 'SUBSCRIBER_IDENTITY'
}

// Main interfaces
export interface EDLEntry {
    id: string;
    address: string;
    comment?: string;
    type: EntryType;
    isEnabled: boolean;
    createdAt: string;
    updatedAt: string;
    createdBy?: string;
    listId: string;
    list?: EDL;
}

export interface EDL {
    id: string;
    name: string;
    description?: string;
    type: ListType;
    entries?: EDLEntry[];
    createdAt: string;
    updatedAt: string;
    createdBy?: string;
}

// DTOs for creating/updating
export interface CreateEdlListDto {
    name: string;
    description?: string;
    type: ListType;
    createdBy?: string;
}

export interface CreateEdlEntryDto {
    address: string;
    comment?: string;
    type: EntryType;
    isEnabled?: boolean;
    createdBy?: string;
}

export interface UpdateEdlListDto extends Partial<CreateEdlListDto> {}

export interface UpdateEdlEntryDto extends Partial<CreateEdlEntryDto> {
    listId?: string;
}

// View model for the table display
export interface EDLViewModel {
    id: string;
    name: string;
    description?: string;
    type: ListType;
    entryCount: number;
    lastUpdated: string;
}
