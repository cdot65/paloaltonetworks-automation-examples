import { HttpClient, HttpHeaders } from "@angular/common/http";
import { Observable, of } from "rxjs";

import { Injectable } from "@angular/core";
import { catchError } from "rxjs/operators";
import { environment } from "../../../environments/environment.prod";

@Injectable({
    providedIn: "root",
})
export class AiService {
    private API_URL = environment.apiUrl;

    constructor(private http: HttpClient) {}

    fetchAiData(): Observable<any[]> {
        return this.http.get<any[]>(`${this.API_URL}/api/v1/ai/`).pipe(
            catchError((error) => {
                console.error("Error fetching ChatGPT data:", error);
                return of([]);
            })
        );
    }

    sendScript(scriptDetails: any): Observable<any> {
        const headers = new HttpHeaders({ "Content-Type": "application/json" });
        return this.http
            .post<any>(
                `${this.API_URL}/api/v1/ai/create-script`,
                scriptDetails,
                {
                    headers: headers,
                }
            )
            .pipe(
                catchError((error) => {
                    console.error("Error sending script:", error);
                    return of(null);
                })
            );
    }

    sendChangeAnalysis(comparisonDetails: any): Observable<any> {
        const headers = new HttpHeaders({ "Content-Type": "application/json" });
        return this.http
            .post<any>(
                `${this.API_URL}/api/v1/ai/change-analysis`,
                comparisonDetails,
                {
                    headers: headers,
                }
            )
            .pipe(
                catchError((error) => {
                    console.error("Error sending script:", error);
                    return of(null);
                })
            );
    }
}
