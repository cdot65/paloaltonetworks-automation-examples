import { HttpClient, HttpHeaders } from "@angular/common/http";
import { Observable, of } from "rxjs";

import { CookieService } from "ngx-cookie-service";
import { Injectable } from "@angular/core";
import { catchError } from "rxjs/operators";
import { environment } from "../../../environments/environment.prod";

@Injectable({
    providedIn: "root",
})
export class JobsService {
    private authToken: string;
    private headers: HttpHeaders;
    private API_URL = environment.apiUrl;

    constructor(
        private http: HttpClient,
        private cookieService: CookieService
    ) {
        this.authToken = this.cookieService.get("auth_token");
        this.headers = new HttpHeaders().set(
            "Authorization",
            `Token ${this.authToken}`
        );
    }

    fetchJobsData(): Observable<any[]> {
        return this.http.get<any[]>(this.API_URL + "/api/v1/jobs").pipe(
            catchError((error) => {
                console.error("Error fetching Jobs data:", error);
                return of([]);
            })
        );
    }

    getJobDetails(taskId: string): Observable<any> {
        return this.http
            .get(`${this.API_URL}` + "/api/v1/jobs/" + `${taskId}/`, {
                headers: this.headers,
            })
            .pipe(
                catchError((error) => {
                    console.error("Error fetching Job details:", error);
                    return of(null);
                })
            );
    }
}
