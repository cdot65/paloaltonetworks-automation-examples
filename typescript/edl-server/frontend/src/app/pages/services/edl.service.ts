// src/app/pages/services/edl.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environmentProd } from '../../../environments/environment';
import {
    EDL,
    EdlEntry,
    CreateEdlListDto,
    CreateEdlEntryDto
} from '../interfaces/edl.interface';

@Injectable({
    providedIn: 'root'
})
export class EdlService {
    private readonly apiUrl = `${environmentProd.apiUrl}/edl`;
    private readonly headers = new HttpHeaders({
        'Content-Type': 'application/json'
    });

    constructor(private http: HttpClient) {}

    // EDL List Operations
    createEdlList(edlList: CreateEdlListDto): Observable<EDL> {
        return this.http.post<EDL>(
            `${this.apiUrl}/lists`,
            edlList,
            { headers: this.headers }
        );
    }

    getAllEdlLists(): Observable<EDL[]> {
        return this.http.get<EDL[]>(
            `${this.apiUrl}/lists`,
            { headers: this.headers }
        );
    }

    getEdlListByName(name: string): Observable<EDL> {
        return this.http.get<EDL>(
            `${this.apiUrl}/lists/${name}`,
            { headers: this.headers }
        );
    }

    // EDL Entry Operations
    createEdlEntry(entry: CreateEdlEntryDto): Observable<EdlEntry> {
        return this.http.post<EdlEntry>(
            `${this.apiUrl}/entries`,
            entry,
            { headers: this.headers }
        );
    }

    getEntriesByListName(listName: string): Observable<EdlEntry[]> {
        return this.http.get<EdlEntry[]>(
            `${this.apiUrl}/entries?listName=${listName}`,
            { headers: this.headers }
        );
    }

    updateEntry(id: string, entry: Partial<EdlEntry>): Observable<EdlEntry> {
        return this.http.patch<EdlEntry>(
            `${this.apiUrl}/entries/${id}`,
            entry,
            { headers: this.headers }
        );
    }

    deleteEntry(id: string): Observable<void> {
        return this.http.delete<void>(
            `${this.apiUrl}/entries/${id}`,
            { headers: this.headers }
        );
    }

}
