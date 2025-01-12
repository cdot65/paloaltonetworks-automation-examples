// backend/src/edl/interfaces/edl.interface.ts
import { ListType, EntryType } from '../types/edl.types';

export interface EdlEntry {
    id: string;
    address: string;
    comment?: string;
    type: EntryType;
    isEnabled: boolean;
    createdAt: Date;
    updatedAt: Date;
    createdBy?: string;
    listName: string; // Changed from listId
    list?: EdlList;
}

export interface EdlList {
    id: string;
    name: string;
    description?: string;
    type: ListType;
    entries?: EdlEntry[];
    createdAt: Date;
    updatedAt: Date;
    createdBy?: string;
}
