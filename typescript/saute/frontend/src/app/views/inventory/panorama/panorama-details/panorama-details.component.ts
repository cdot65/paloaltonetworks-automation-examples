import {
    AbstractControl,
    AsyncValidatorFn,
    FormBuilder,
    FormControl,
    FormGroup,
    ValidationErrors,
    Validators,
} from "@angular/forms";
/**
 * PanoramaDetailsComponent handles displaying and updating panorama entries.
 */
import { ActivatedRoute, Router } from "@angular/router";
import { Component, OnInit } from "@angular/core";
import {
    Panorama,
    PanoramaPlatform,
} from "../../../../shared/interfaces/panorama.interface";
import { debounceTime, first, map, switchMap } from "rxjs/operators";
import { distinctUntilChanged, of, timer } from "rxjs";

import { Observable } from "rxjs";
import { PanoramaService } from "../../../../shared/services/panorama.service";

@Component({
    selector: "app-panorama-details",
    templateUrl: "./panorama-details.component.html",
})

/**
 * PanoramaDetailsComponent is an Angular component for displaying and updating
 * an individual panorama entry based on its identifier (UUID).
 */
export class PanoramaDetailsComponent implements OnInit {
    // Form group for the panorama entry form
    panoramaForm!: FormGroup;
    // Unique identifier (UUID) for the panorama
    uuid!: string;
    panoramaExistsErrorMessage = "";
    panorama: Panorama | undefined;
    panoramaPlatforms$!: Observable<PanoramaPlatform[]>;

    /**
     * Constructor for the PanoramaDetailsComponent. Initializes the form group
     * and injects required services and modules.
     */
    constructor(
        private route: ActivatedRoute,
        private router: Router,
        private panoramaService: PanoramaService
    ) {
        this.editForm();
    }

    // Angular lifecycle hook that initializes the component
    ngOnInit(): void {
        this.panoramaPlatforms$ = this.panoramaService.fetchPanoramaPlatforms();

        this.route.params.subscribe((params) => {
            this.uuid = params["id"];
            this.fetchPanoramaData();
        });
    }

    /**
     * Initializes the panoramaForm FormGroup with default form controls.
     */
    editForm(): void {
        this.panoramaForm = new FormGroup({
            api_key: new FormControl(""),
            hostname: new FormControl(""),
            ipv4_address: new FormControl(""),
            ipv6_address: new FormControl(""),
            notes: new FormControl(""),
            platform: new FormControl(null),
        });
    }

    /**
     * Fetches the panorama data and sets it to the panoramaForm FormGroup
     * based on the provided UUID.
     */
    fetchPanoramaData(): void {
        this.panoramaService
            .panoramaInventory()
            .subscribe((data: Panorama[]) => {
                this.panorama = data.find((i) => i.uuid === this.uuid);
                if (this.panorama) {
                    this.panoramaForm.setValue({
                        api_key: this.panorama.api_key,
                        hostname: this.panorama.hostname,
                        ipv4_address: this.panorama.ipv4_address,
                        ipv6_address: this.panorama.ipv6_address,
                        notes: this.panorama.notes || "",
                        platform: this.panorama.platform,
                    });
                }
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
     * Updates an existing panorama entry with the provided data.
     * Redirects to the "/inventory/panorama/" route on successful update.
     *
     * @param updatedEntry - The updated panorama data to be submitted
     */
    updateEntry(updatedEntry: Panorama): void {
        if (this.panoramaForm.valid && this.uuid) {
            this.panoramaService
                .updatePanorama(updatedEntry, this.uuid)
                .subscribe({
                    next: () => {
                        this.router.navigate(["/inventory/panorama/"]);
                    },
                    error: (error: any) => {
                        console.error("Error updating entry:", error);
                    },
                });
        } else {
            console.error("Form is invalid");
        }
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
