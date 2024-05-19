import {
    ActivatedRouteSnapshot,
    CanActivate,
    Router,
    RouterStateSnapshot,
} from "@angular/router";

import { CookieService } from "ngx-cookie-service";
import { Injectable } from "@angular/core";
import { Observable } from "rxjs";

@Injectable({
    providedIn: "root",
})
export class AuthGuard implements CanActivate {
    constructor(private router: Router, private cookieService: CookieService) {}

    canActivate(
        route: ActivatedRouteSnapshot,
        state: RouterStateSnapshot
    ): Observable<boolean> | Promise<boolean> | boolean {
        const authToken = this.cookieService.get("auth_token");

        if (authToken) {
            return true;
        } else {
            this.router.navigate(["/login"]);
            return false;
        }
    }
}
