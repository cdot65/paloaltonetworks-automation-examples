import { HttpClient, HttpHeaders } from "@angular/common/http";
import { Observable, interval, of } from "rxjs";

import { Injectable } from "@angular/core";
import { catchError } from "rxjs/operators";
import { environment } from "../../../environments/environment.prod";
import { switchMap } from "rxjs/operators";

@Injectable({
    providedIn: "root",
})
export class BotResponseService {
    private API_URL = environment.apiUrl;

    constructor(private http: HttpClient) {}

    pollBotResponses(conversationId: string): Observable<any> {
        // console.log("pollBotResponses called with conversationId:", conversationId);

        return interval(2000).pipe(
            switchMap(() => this.getBotResponse(conversationId))
        );
    }

    private getBotResponse(conversationId: string): Observable<any> {
        // console.log("getBotResponse called with conversationId:", conversationId);
        return this.http.get(
            `${this.API_URL}/api/v1/ai/messages/${conversationId}`
        );
    }

    generateResponse(chatDetails: any): Observable<any> {
        const headers = new HttpHeaders({ "Content-Type": "application/json" });
        return this.http
            .post<any>(`${this.API_URL}/api/v1/ai/chat`, chatDetails, {
                headers: headers,
            })
            .pipe(
                catchError((error) => {
                    console.error("Error generating chat response:", error);
                    return of(null);
                })
            );
    }
}
