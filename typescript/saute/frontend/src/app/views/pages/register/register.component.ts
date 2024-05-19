import { AuthService } from "../../../auth.service";
import { Component } from "@angular/core";
import { MatSnackBar } from "@angular/material/snack-bar";
import { NgForm } from "@angular/forms";
import { Router } from "@angular/router";

@Component({
    selector: "app-register",
    templateUrl: "./register.component.html",
    styleUrls: ["./register.component.scss"],
})
export class RegisterComponent {
    username: string = "";
    email: string = "";
    password1: string = "";
    password2: string = "";

    constructor(
        private authService: AuthService,
        private router: Router,
        private snackBar: MatSnackBar
    ) {}

    onSubmit(form: NgForm) {
        const { username, email, password1, password2 } = form.value;
        // console.log("Form data:", { username, email, password1, password2 }); // Log the form data
        this.authService
            .register(username, email, password1, password2)
            .subscribe({
                next: (response) => {
                    // console.log("Registration response:", response); // Log the response
                    // Navigate to the login page after successful registration
                    this.router.navigate(["/login"]);

                    // Display a success message
                    this.snackBar.open(
                        "Account created successfully",
                        "Close",
                        {
                            duration: 3000,
                        }
                    );
                },
                error: (error) => {
                    console.error("Registration error:", error); // Log the error
                    // Handle the error and display the error message
                    const errorMessage =
                        error.error?.detail || "Registration failed";
                    this.snackBar.open(errorMessage, "Close", {
                        duration: 3000,
                    });
                },
            });
    }
}
