import { Firewall, FirewallPlatform } from "../interfaces/firewall.interface";
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { Observable, of } from "rxjs";

import { CookieService } from "ngx-cookie-service";
import { Injectable } from "@angular/core";
import { catchError } from "rxjs/operators";
import { environment } from "../../../environments/environment.prod";
import { map } from "rxjs/operators";

@Injectable({
    providedIn: "root",
})
/**
 * FirewallService is responsible for performing CRUD operations
 * related to Firewalls through HTTP requests to the server-side API.
 *
 * This class provides services to interact with the firewall endpoint of the backend API.
 */
export class FirewallService {
    private API_URL = environment.apiUrl;

    constructor(
        private http: HttpClient,
        private cookieService: CookieService
    ) {}

    /**
     * Fetches all firewall data from the backend API.
     *
     * @returns {Observable<Firewall[]>} - An observable stream of firewall data.
     */
    fetchFirewallData(): Observable<Firewall[]> {
        return this.http
            .get<Firewall[]>(`${this.API_URL}/api/v1/firewalls/`)
            .pipe(
                map((firewalls: Firewall[]) => {
                    return firewalls.sort((a, b) =>
                        a.hostname.localeCompare(b.hostname)
                    );
                }),
                catchError((error) => {
                    console.error("Error fetching Firewall data:", error);
                    return of([]);
                })
            );
    }

    /**
     * Checks if an firewall with the given name exists in the backend API.
     *
     * @param {string} name - The name of the firewall.
     * @returns {Observable<boolean>} - An observable stream indicating the existence of the firewall.
     */
    firewallExists(hostname: string): Observable<boolean> {
        let formattedValue = hostname.toLowerCase().replace(/[\s-]/g, "_");
        return this.http
            .get<boolean>(
                `${this.API_URL}/api/v1/firewall/exists?hostname=${hostname}&formatted_value=${formattedValue}`
            )
            .pipe(
                catchError((error) => {
                    console.error("Error checking firewall:", error);
                    return of(false);
                })
            );
    }

    /**
     * Sends a request to the backend API to create a new firewall.
     *
     * @param {Firewall} firewall - The firewall data.
     * @returns {Observable<Firewall>} - An observable stream containing the created firewall data.
     */
    createFirewall(firewall: Firewall): Observable<Firewall> {
        const authToken = this.cookieService.get("auth_token");
        const headers = new HttpHeaders().set(
            "Authorization",
            `Token ${authToken}`
        );
        return this.http
            .post<Firewall>(`${this.API_URL}/api/v1/firewalls/`, firewall, {
                headers,
            })
            .pipe(
                catchError((error) => {
                    console.error("Error creating firewall:", error);
                    throw error; // Just rethrow the error
                })
            );
    }

    /**
     * Sends a request to the backend API to update an existing firewall.
     *
     * @param {Firewall} firewall - The firewall data to be updated.
     * @param {string} uuid - The unique identifier of the firewall to be updated.
     * @returns {Observable<Firewall>} - An observable stream containing the updated firewall data.
     */
    updateFirewall(firewall: Firewall, uuid: string): Observable<Firewall> {
        const authToken = this.cookieService.get("auth_token");
        const headers = new HttpHeaders().set(
            "Authorization",
            `Token ${authToken}`
        );
        return this.http
            .patch<Firewall>(
                `${this.API_URL}/api/v1/firewalls/${uuid}/`,
                firewall,
                {
                    headers,
                }
            )
            .pipe(
                catchError((error: any) => {
                    console.error("Error updating firewall:", error);
                    throw error;
                })
            );
    }

    /**
     * Sends a request to the backend API to delete an existing firewall.
     * @param {string} uuid - The unique identifier of the firewall to be deleted.
     * @returns {Observable<any>} - An observable stream containing the response from the backend API.
     * The response is null if the firewall was successfully deleted.
     * Otherwise, the response contains an error message.
     */
    deleteEntry(uuid: string): Observable<any> {
        const authToken = this.cookieService.get("auth_token");
        const headers = new HttpHeaders().set(
            "Authorization",
            `Token ${authToken}`
        );
        return this.http
            .delete(`${this.API_URL}/api/v1/firewalls/${uuid}/`, { headers })
            .pipe(
                catchError((error) => {
                    console.error("Error deleting Firewall instance:", error);
                    return of(null);
                })
            );
    }

    /**
     * Fetches all firewall types from the backend API, sorts them alphabetically,
     * and returns them as an observable stream of firewall type data.
     *
     * @returns {Observable<FirewallPlatform[]>} An observable stream of alphabetically sorted firewall type data.
     */
    fetchFirewallPlatforms(): Observable<FirewallPlatform[]> {
        return this.http
            .get<FirewallPlatform[]>(`${this.API_URL}/api/v1/firewall/types/`)
            .pipe(
                map((types: FirewallPlatform[]) =>
                    types.sort((a, b) => a.name.localeCompare(b.name))
                ),
                catchError((error) => {
                    console.error("Error fetching Firewall types:", error);
                    return of([]);
                })
            );
    }

    executeAdminReport(jobDetails: any): Observable<any> {
        const headers = new HttpHeaders({ "Content-Type": "application/json" });
        return this.http
            .post<any>(
                `${this.API_URL}/api/v1/assessment/admin-report`,
                jobDetails,
                {
                    headers: headers,
                }
            )
            .pipe(
                catchError((error) => {
                    console.error("Error executing request:", error);
                    return of(null);
                })
            );
    }
}
