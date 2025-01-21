import {
    HttpEvent,
    HttpHandler,
    HttpInterceptor,
    HttpRequest,
} from "@angular/common/http";

import { CookieService } from "ngx-cookie-service";
import { Injectable } from "@angular/core";
import { Observable } from "rxjs";
import { environment } from "../environments/environment.prod";

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
    constructor(private cookieService: CookieService) {}

    intercept(
        request: HttpRequest<any>,
        next: HttpHandler
    ): Observable<HttpEvent<any>> {
        const authToken = this.cookieService.get("auth_token");
        if (
            authToken &&
            request.url !== `${environment.apiUrl}${environment.tokenUrl}`
        ) {
            request = request.clone({
                setHeaders: {
                    Authorization: `Token ${authToken}`,
                },
            });
        }
        return next.handle(request);
    }
}
