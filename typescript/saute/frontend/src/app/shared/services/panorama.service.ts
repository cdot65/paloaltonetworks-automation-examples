import { HttpClient, HttpHeaders } from "@angular/common/http";
import { Observable, of } from "rxjs";
import { Panorama, PanoramaPlatform } from "../interfaces/panorama.interface";

import { CookieService } from "ngx-cookie-service";
import { Injectable } from "@angular/core";
import { catchError } from "rxjs/operators";
import { environment } from "../../../environments/environment.prod";
import { map } from "rxjs/operators";

@Injectable({
    providedIn: "root",
})
/**
 * PanoramaService is responsible for performing CRUD operations
 * related to Panoramas through HTTP requests to the server-side API.
 *
 * This class provides services to interact with the panorama endpoint of the backend API.
 */
export class PanoramaService {
    private API_URL = environment.apiUrl;

    constructor(
        private http: HttpClient,
        private cookieService: CookieService
    ) {}

    /**
     * Fetches all panorama data from the backend API.
     *
     * @returns {Observable<Panorama[]>} - An observable stream of panorama data.
     */
    panoramaInventory(): Observable<Panorama[]> {
        return this.http
            .get<Panorama[]>(`${this.API_URL}/api/v1/panorama/inventory/`)
            .pipe(
                map((panoramas: Panorama[]) => {
                    return panoramas.sort((a, b) =>
                        a.hostname.localeCompare(b.hostname)
                    );
                }),
                catchError((error) => {
                    console.error("Error fetching Panorama data:", error);
                    return of([]);
                })
            );
    }

    /**
     * Checks if an panorama with the given name exists in the backend API.
     *
     * @param {string} name - The name of the panorama.
     * @returns {Observable<boolean>} - An observable stream indicating the existence of the panorama.
     */
    panoramaExists(hostname: string): Observable<boolean> {
        let formattedValue = hostname.toLowerCase().replace(/[\s-]/g, "_");
        return this.http
            .get<boolean>(
                `${this.API_URL}/api/v1/panorama/exists?hostname=${hostname}&formatted_value=${formattedValue}`
            )
            .pipe(
                catchError((error) => {
                    console.error("Error checking panorama:", error);
                    return of(false);
                })
            );
    }

    /**
     * Sends a request to the backend API to create a new panorama.
     *
     * @param {Panorama} panorama - The panorama data.
     * @returns {Observable<Panorama>} - An observable stream containing the created panorama data.
     */
    createPanorama(panorama: Panorama): Observable<Panorama> {
        const authToken = this.cookieService.get("auth_token");
        const headers = new HttpHeaders().set(
            "Authorization",
            `Token ${authToken}`
        );
        return this.http
            .post<Panorama>(
                `${this.API_URL}/api/v1/panorama/inventory/`,
                panorama,
                {
                    headers,
                }
            )
            .pipe(
                catchError((error) => {
                    console.error("Error creating panorama:", error);
                    throw error; // Just rethrow the error
                })
            );
    }

    /**
     * Sends a request to the backend API to update an existing panorama.
     *
     * @param {Panorama} panorama - The panorama data to be updated.
     * @param {string} uuid - The unique identifier of the panorama to be updated.
     * @returns {Observable<Panorama>} - An observable stream containing the updated panorama data.
     */
    updatePanorama(panorama: Panorama, uuid: string): Observable<Panorama> {
        const authToken = this.cookieService.get("auth_token");
        const headers = new HttpHeaders().set(
            "Authorization",
            `Token ${authToken}`
        );
        return this.http
            .patch<Panorama>(
                `${this.API_URL}/api/v1/panorama/inventory/${uuid}/`,
                panorama,
                {
                    headers,
                }
            )
            .pipe(
                catchError((error: any) => {
                    console.error("Error updating panorama:", error);
                    throw error;
                })
            );
    }

    /**
     * Sends a request to the backend API to delete an existing panorama.
     * @param {string} uuid - The unique identifier of the panorama to be deleted.
     * @returns {Observable<any>} - An observable stream containing the response from the backend API.
     * The response is null if the panorama was successfully deleted.
     * Otherwise, the response contains an error message.
     */
    deleteEntry(uuid: string): Observable<any> {
        const authToken = this.cookieService.get("auth_token");
        const headers = new HttpHeaders().set(
            "Authorization",
            `Token ${authToken}`
        );
        return this.http
            .delete(`${this.API_URL}/api/v1/panorama/inventory/${uuid}/`, {
                headers,
            })
            .pipe(
                catchError((error) => {
                    console.error("Error deleting Panorama instance:", error);
                    return of(null);
                })
            );
    }

    /**
     * Fetches all panorama types from the backend API, sorts them alphabetically,
     * and returns them as an observable stream of panorama type data.
     *
     * @returns {Observable<PanoramaPlatform[]>} An observable stream of alphabetically sorted panorama type data.
     */
    fetchPanoramaPlatforms(): Observable<PanoramaPlatform[]> {
        return this.http
            .get<PanoramaPlatform[]>(`${this.API_URL}/api/v1/panorama/types/`)
            .pipe(
                map((types: PanoramaPlatform[]) =>
                    types.sort((a, b) => a.name.localeCompare(b.name))
                ),
                catchError((error) => {
                    console.error("Error fetching Panorama types:", error);
                    return of([]);
                })
            );
    }

    postSoftwareInformation(softwareInformation: any): Observable<any> {
        const headers = new HttpHeaders({ "Content-Type": "application/json" });
        return this.http
            .post<any>(
                `${this.API_URL}/api/v1/report/get-system-info`,
                softwareInformation,
                { headers: headers }
            )
            .pipe(
                catchError((error) => {
                    console.error("Error posting software information:", error);
                    return of(null);
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
