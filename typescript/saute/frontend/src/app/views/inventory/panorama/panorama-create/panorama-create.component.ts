import {
    AbstractControl,
    AsyncValidatorFn,
    ValidationErrors,
} from "@angular/forms";
import { Component, OnInit } from "@angular/core";
import { FormBuilder, FormGroup, Validators } from "@angular/forms";
import {
    Panorama,
    PanoramaPlatform,
} from "../../../../shared/interfaces/panorama.interface";
import { debounceTime, first, map, switchMap } from "rxjs/operators";
import { distinctUntilChanged, of, timer } from "rxjs";

import { AuthService } from "../../../../shared/services/auth.service";
import { Observable } from "rxjs";
import { PanoramaService } from "../../../../shared/services/panorama.service";
import { Router } from "@angular/router";

/**
 * @class PanoramaCreateComponent
 *
 * This Angular component provides functionality to create a new panorama.
 * It initializes and manages a FormGroup for the new panorama's data,
 * validates this data (asynchronously checking whether an panorama with the given name exists),
 * and handles form submission, i.e., sending the new panorama data to the PanoramaService
 * and managing the server's response.
 * Additionally, it handles form cancellation, i.e., navigation back to the panorama list.
 */
@Component({
    selector: "app-panorama-create",
    templateUrl: "./panorama-create.component.html",
})

/**
 * @class PanoramaCreateComponent
 *
 * This class represents the component responsible for creating new panorama.
 * It handles form creation, input validation, form submission and user redirection.
 */
export class PanoramaCreateComponent implements OnInit {
    panoramaForm: FormGroup;
    private lastPanoramaName = "";
    panoramaExistsErrorMessage = "";
    panoramaPlatforms$!: Observable<PanoramaPlatform[]>;

    constructor(
        private panoramaService: PanoramaService,
        private authService: AuthService,
        private router: Router,
        private fb: FormBuilder
    ) {
        // Create the form group for the panorama creation form
        this.panoramaForm = this.fb.group({
            api_key: [""],
            hostname: [
                "",
                Validators.required,
                this.checkPanoramaExists(this.panoramaService),
            ],
            ipv4_address: [""],
            ipv6_address: [""],
            platform: [""],
            notes: [""],
            author: ["", Validators.required],
        });

        // Subscribe to changes in the 'name' field and update its validation status
        this.panoramaForm
            .get("name")
            ?.valueChanges.pipe(debounceTime(500), distinctUntilChanged())
            .subscribe((value) => {
                this.lastPanoramaName = value;
                this.panoramaForm.get("name")?.updateValueAndValidity();
            });
    }

    // Angular lifecycle hook that initializes the component
    ngOnInit(): void {
        // Fetch the user's data and initialize form validators upon component initialization
        this.getUserData();

        // Fetch the types of Panorama
        this.fetchPanoramaPlatforms();
    }

    /**
     * Retrieve the user data from the AuthService and update the 'author' field in the form.
     */
    getUserData() {
        this.authService.getUserData().subscribe({
            next: (userData) => {
                this.panoramaForm.patchValue({ author: userData.pk });
                this.panoramaForm.updateValueAndValidity();
            },
            error: (error) => {
                console.error("Error getting user data:", error);
            },
        });
    }

    /**
     * Create an async validator function that checks if the panorama already exists in the database.
     *
     * @param {PanoramaService} panoramaService - The service to use to check if the panorama exists.
     * @returns {AsyncValidatorFn} - The validator function.
     */
    checkPanoramaExists(panoramaService: PanoramaService): AsyncValidatorFn {
        return (
            control: AbstractControl
        ): Observable<ValidationErrors | null> => {
            if (!control.value || control.value.trim() === "") {
                return of(null); // No validation error if the control value is empty or only spaces
            } else {
                return timer(500).pipe(
                    switchMap(() => {
                        let formattedValue = control.value
                            .toLowerCase()
                            .replace(/[\s-]/g, "_");

                        return panoramaService
                            .panoramaExists(formattedValue)
                            .pipe(
                                map((res: any) => {
                                    if (res.exists) {
                                        this.panoramaExistsErrorMessage =
                                            "This panorama already exists";
                                        return { panoramaExists: true };
                                    } else {
                                        this.panoramaExistsErrorMessage = "";
                                        return null;
                                    }
                                })
                            );
                    })
                );
            }
        };
    }

    /**
     * Returns true if the 'name' control is invalid and has the 'panoramaExists' error.
     */
    isPending(controlName: string): boolean {
        return this.panoramaForm.get(controlName)?.status === "PENDING";
    }

    /**
     * Returns list of panorama types to be used in the dropdown menu.
     */
    fetchPanoramaPlatforms(): void {
        this.panoramaPlatforms$ = this.panoramaService.fetchPanoramaPlatforms();
    }

    /**
     * Handles the form submission event. It validates the form, logs the form value and validity,
     * submits the new panorama to the PanoramaService, handles the server's response, and navigates
     * the user back to the panorama list upon successful creation.
     */
    onSubmit() {
        if (this.panoramaForm.valid) {
            const panorama: Panorama = this.panoramaForm.value as Panorama;
            this.panoramaService.createPanorama(panorama).subscribe({
                next: (response) => {
                    // console.log("New panorama created:", response);
                    this.resetForm();
                    this.router.navigate(["/inventory/panorama/"]);
                },
                error: (error) => {
                    console.error("Error creating panorama:", error);
                },
            });
        } else {
            console.error("Form is invalid");
        }
    }

    /**
     * Reset the form values.
     */
    resetForm() {
        this.panoramaForm.reset();
    }

    /**
     * Handles the form cancellation event and navigates the user back to the panorama list.
     */
    onCancel(): void {
        this.router.navigate(["/inventory/panorama/"]);
    }
}
