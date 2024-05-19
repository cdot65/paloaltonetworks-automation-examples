import { AuthService } from "../../../auth.service";
import { Component } from "@angular/core";
import { CookieService } from "ngx-cookie-service";
import { MatSnackBar } from "@angular/material/snack-bar";
import { NgForm } from "@angular/forms";
import { Router } from "@angular/router";
import { UserProfileService } from "../../../shared/services/user-profile.service";

@Component({
    selector: "app-login",
    templateUrl: "./login.component.html",
    styleUrls: ["./login.component.scss"],
})
export class LoginComponent {
    username: string = "";
    password: string = "";
    errorMessage: string = "";

    constructor(
        private router: Router,
        private authService: AuthService,
        private cookieService: CookieService,
        private snackBar: MatSnackBar,
        private userProfileService: UserProfileService
    ) {}

    onSubmit(form: NgForm) {
        // reset the error message
        this.errorMessage = "";

        const { username, password } = form.value;
        this.authService.login(username, password).subscribe({
            next: (response) => {
                // Set the auth_token cookie and navigate to the home route
                this.cookieService.set("auth_token", response.key);
                this.router.navigate(["/"]);

                // Update the user profile image URL
                this.userProfileService.updateProfileImageUrl();

                // Display a success message
                this.snackBar.open("Logged in successfully", "Close", {
                    duration: 3000,
                });
            },
            error: (error) => {
                // Handle the error and display the error message
                this.errorMessage = "Invalid username or password";
            },
        });
    }
}
