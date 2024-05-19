import { Component, OnInit } from "@angular/core";
import { HttpClient, HttpHeaders } from "@angular/common/http";

import { CookieService } from "ngx-cookie-service";
import { NgForm } from "@angular/forms";
import { Router } from "@angular/router";
import { environment } from "../../../../../environments/environment.prod";
import { firstValueFrom } from "rxjs";

@Component({
    selector: "app-prisma-create",
    templateUrl: "./prisma-create.component.html",
})
export class PrismaCreateComponent implements OnInit {
    private API_URL = environment.apiUrl;
    prisma = {
        tenant_name: "",
        client_id: "",
        tsg_id: "",
        client_secret: "",
        author: "",
    };

    constructor(
        private http: HttpClient,
        private cookieService: CookieService,
        private router: Router
    ) {}

    ngOnInit(): void {
        this.getUserData();
    }

    async getUserData() {
        const authToken = this.cookieService.get("auth_token");
        const headers = new HttpHeaders().set(
            "Authorization",
            `Token ${authToken}`
        );

        try {
            const response: any = await firstValueFrom(
                this.http.get(`${this.API_URL}/api/v1/dj-rest-auth/user/`, {
                    headers,
                })
            );
            this.prisma.author = response.pk;
        } catch (error) {
            console.error("Error getting user data:", error);
        }
    }

    onSubmit(form: NgForm) {
        if (form.valid) {
            const authToken = this.cookieService.get("auth_token");
            const headers = new HttpHeaders().set(
                "Authorization",
                `Token ${authToken}`
            );

            this.http
                .post(`${this.API_URL}/api/v1/prisma/`, this.prisma, {
                    headers,
                })
                .subscribe({
                    next: (response) => {
                        // console.log("New prisma created:", response);
                        this.resetForm(form);
                        this.router.navigate(["/inventory/prisma/"]);
                    },
                    error: (error) => {
                        console.error("Error creating prisma:", error);
                    },
                });
        } else {
            console.error("Form is invalid");
        }
    }

    resetForm(form: NgForm) {
        form.reset();
    }

    onCancel(): void {
        this.router.navigate(["/inventory/prisma/"]);
    }
}
