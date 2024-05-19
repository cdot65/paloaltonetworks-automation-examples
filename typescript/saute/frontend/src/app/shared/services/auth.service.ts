import { HttpClient, HttpHeaders } from "@angular/common/http";

import { CookieService } from "ngx-cookie-service";
import { Injectable } from "@angular/core";
import { environment } from "../../../environments/environment.prod";
import { map } from "rxjs/operators";

/**
 * @class AuthService
 *
 * This service is responsible for handling operations related to authentication, such as retrieving user data.
 *
 * @property {string} API_URL - The URL of the backend API. It is loaded from the environment variables.
 *
 * @method constructor(http: HttpClient, cookieService: CookieService)
 * @method getUserData(): Observable<any>
 */
@Injectable({
    providedIn: "root",
})
export class AuthService {
    private API_URL = environment.apiUrl; // API endpoint URL retrieved from the environment variables.

    /**
     * @constructor
     * Constructs an AuthService instance.
     *
     * @param {HttpClient} http - The Angular HttpClient for making HTTP requests.
     * @param {CookieService} cookieService - A service for handling browser cookies.
     */
    constructor(
        private http: HttpClient,
        private cookieService: CookieService
    ) {}

    /**
     * Fetches user data from the backend API.
     *
     * The method first retrieves the auth token stored in the browser cookies. It then sets up
     * the HTTP headers for the request, with the Authorization header set to the retrieved token.
     *
     * The request is sent to the 'dj-rest-auth/user/' endpoint of the API, and the resulting Observable
     * is piped through a mapping function that transforms the response. Specifically, it converts the 'pk'
     * field from a string to a number.
     *
     * @returns {Observable<any>} An Observable that, when subscribed to, sends the HTTP request and yields the response data.
     * The returned data is an object representing the user's data, with all the properties from the response and 'pk' converted to a number.
     */
    getUserData() {
        const authToken = this.cookieService.get("auth_token"); // Retrieves auth token from cookies.
        const headers = new HttpHeaders().set(
            "Authorization",
            `Token ${authToken}`
        ); // Sets up HTTP headers.

        return this.http
            .get(`${this.API_URL}/api/v1/dj-rest-auth/user/`, {
                headers,
            })
            .pipe(
                map((response: any) => {
                    return {
                        ...response,
                        pk: Number(response.pk), // Converts 'pk' from string to number.
                    };
                })
            );
    }
}
