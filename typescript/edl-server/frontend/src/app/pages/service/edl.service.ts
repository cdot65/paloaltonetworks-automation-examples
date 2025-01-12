// frontend/src/app/pages/service/edl.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environmentProd } from '../../../environments/environment';
import { EDL, EDLEntry, CreateEdlListDto, CreateEdlEntryDto, UpdateEdlListDto, UpdateEdlEntryDto } from '../interfaces/edl.interface';

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
    getAllEdlLists(): Observable<EDL[]> {
        return this.http.get<EDL[]>(`${this.apiUrl}`, { headers: this.headers });
    }

    createEdlList(edlList: CreateEdlListDto): Observable<EDL> {
        return this.http.post<EDL>(`${this.apiUrl}`, edlList, { headers: this.headers });
    }

    getEdlList(id: string): Observable<EDL> {
        return this.http.get<EDL>(`${this.apiUrl}/${id}`, { headers: this.headers });
    }

    updateEdlList(id: string, edlList: UpdateEdlListDto): Observable<EDL> {
        return this.http.patch<EDL>(`${this.apiUrl}/${id}`, edlList, { headers: this.headers });
    }

    deleteEdlList(id: string): Observable<EDL> {
        return this.http.delete<EDL>(`${this.apiUrl}/${id}`, { headers: this.headers });
    }

    // EDL Entry Operations
    getListEntries(listId: string): Observable<EDLEntry[]> {
        return this.http.get<EDLEntry[]>(`${this.apiUrl}/${listId}/entries`, { headers: this.headers });
    }

    createEntry(listId: string, entry: CreateEdlEntryDto): Observable<EDLEntry> {
        return this.http.post<EDLEntry>(`${this.apiUrl}/${listId}/entries`, entry, { headers: this.headers });
    }

    updateEntry(listId: string, entryId: string, entry: UpdateEdlEntryDto): Observable<EDLEntry> {
        return this.http.patch<EDLEntry>(`${this.apiUrl}/${listId}/entries/${entryId}`, entry, { headers: this.headers });
    }

    deleteEntry(listId: string, entryId: string): Observable<EDLEntry> {
        return this.http.delete<EDLEntry>(`${this.apiUrl}/${listId}/entries/${entryId}`, { headers: this.headers });
    }

    // Special Formats
    getListPlaintext(listId: string): Observable<string> {
        return this.http.get(`${this.apiUrl}/${listId}/plaintext`, {
            headers: this.headers,
            responseType: 'text'
        });
    }
}
