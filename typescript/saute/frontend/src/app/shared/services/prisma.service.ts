import { HttpClient, HttpHeaders } from "@angular/common/http";
import { Observable, of } from "rxjs";

import { Injectable } from "@angular/core";
import { catchError } from "rxjs/operators";
import { environment } from "../../../environments/environment.prod";

@Injectable({
    providedIn: "root",
})
export class PrismaService {
    private API_URL = environment.apiUrl;

    constructor(private http: HttpClient) {}

    prismaInventory(): Observable<any[]> {
        return this.http.get<any[]>(`${this.API_URL}/api/v1/prisma/`).pipe(
            catchError((error) => {
                console.error("Error fetching Prisma data:", error);
                return of([]);
            })
        );
    }

    postSyncInformation(syncInformation: any): Observable<any> {
        const headers = new HttpHeaders({ "Content-Type": "application/json" });
        return this.http
            .post<any>(
                `${this.API_URL}/api/v1/configuration/pan-to-prisma`,
                syncInformation,
                { headers: headers }
            )
            .pipe(
                catchError((error) => {
                    console.error("Error posting software information:", error);
                    return of(null);
                })
            );
    }
}
