import { HttpClient, HttpHeaders } from "@angular/common/http";
import { Observable, of } from "rxjs";

import { Injectable } from "@angular/core";
import { catchError } from "rxjs/operators";
import { environment } from "../../../environments/environment.prod";
import { map } from "rxjs/operators";

@Injectable({
    providedIn: "root",
})
export class ScriptService {
    private API_URL = environment.apiUrl;

    constructor(private http: HttpClient) {}

    // Method to fetch all scripts
    fetchScripts(): Observable<any[]> {
        return this.http.get<any[]>(`${this.API_URL}/api/v1/scripts/`).pipe(
            catchError((error) => {
                console.error("Error fetching scripts:", error);
                return of([]);
            })
        );
    }

    fetchScriptByName(name: string): Observable<any> {
        return this.http
            .get<any[]>(`${this.API_URL}/api/v1/scripts/?name=${name}`)
            .pipe(
                map((scripts) => (scripts.length > 0 ? scripts[0] : null)),
                catchError((error) => {
                    console.error(
                        `Error fetching script with name ${name}:`,
                        error
                    );
                    return of(null);
                })
            );
    }
}
