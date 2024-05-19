import {
    AbstractControl,
    AsyncValidatorFn,
    ValidationErrors,
} from "@angular/forms";
import { Component, OnInit } from "@angular/core";
import {
    Firewall,
    FirewallPlatform,
} from "../../../../shared/interfaces/firewall.interface";
import { FormBuilder, FormGroup, Validators } from "@angular/forms";
import { debounceTime, first, map, switchMap } from "rxjs/operators";
import { distinctUntilChanged, of, timer } from "rxjs";

import { AuthService } from "../../../../shared/services/auth.service";
import { FirewallService } from "../../../../shared/services/firewall.service";
import { Observable } from "rxjs";
import { Router } from "@angular/router";

/**
 * @class FirewallCreateComponent
 *
 * This Angular component provides functionality to create a new firewall.
 * It initializes and manages a FormGroup for the new firewall's data,
 * validates this data (asynchronously checking whether an firewall with the given name exists),
 * and handles form submission, i.e., sending the new firewall data to the FirewallService
 * and managing the server's response.
 * Additionally, it handles form cancellation, i.e., navigation back to the firewall list.
 */
@Component({
    selector: "app-firewall-create",
    templateUrl: "./firewall-create.component.html",
})

/**
 * @class FirewallCreateComponent
 *
 * This class represents the component responsible for creating new firewall.
 * It handles form creation, input validation, form submission and user redirection.
 */
export class FirewallCreateComponent implements OnInit {
    firewallForm: FormGroup;
    private lastFirewallName = "";
    firewallExistsErrorMessage = "";
    firewallPlatforms$!: Observable<FirewallPlatform[]>;

    constructor(
        private firewallService: FirewallService,
        private authService: AuthService,
        private router: Router,
        private fb: FormBuilder
    ) {
        // Create the form group for the firewall creation form
        this.firewallForm = this.fb.group({
            api_key: [""],
            hostname: [
                "",
                Validators.required,
                this.checkFirewallExists(this.firewallService),
            ],
            ipv4_address: [""],
            ipv6_address: [""],
            platform: [""],
            notes: [""],
            author: ["", Validators.required],
        });

        // Subscribe to changes in the 'name' field and update its validation status
        this.firewallForm
            .get("name")
            ?.valueChanges.pipe(debounceTime(500), distinctUntilChanged())
            .subscribe((value) => {
                this.lastFirewallName = value;
                this.firewallForm.get("name")?.updateValueAndValidity();
            });
    }

    // Angular lifecycle hook that initializes the component
    ngOnInit(): void {
        // Fetch the user's data and initialize form validators upon component initialization
        this.getUserData();

        // Fetch the types of Firewall
        this.fetchFirewallPlatforms();
    }

    /**
     * Retrieve the user data from the AuthService and update the 'author' field in the form.
     */
    getUserData() {
        this.authService.getUserData().subscribe({
            next: (userData) => {
                this.firewallForm.patchValue({ author: userData.pk });
                this.firewallForm.updateValueAndValidity();
            },
            error: (error) => {
                console.error("Error getting user data:", error);
            },
        });
    }

    /**
     * Create an async validator function that checks if the firewall already exists in the database.
     *
     * @param {FirewallService} firewallService - The service to use to check if the firewall exists.
     * @returns {AsyncValidatorFn} - The validator function.
     */
    checkFirewallExists(firewallService: FirewallService): AsyncValidatorFn {
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

                        return firewallService
                            .firewallExists(formattedValue)
                            .pipe(
                                map((res: any) => {
                                    if (res.exists) {
                                        this.firewallExistsErrorMessage =
                                            "This firewall already exists";
                                        return { firewallExists: true };
                                    } else {
                                        this.firewallExistsErrorMessage = "";
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
     * Returns true if the 'name' control is invalid and has the 'firewallExists' error.
     */
    isPending(controlName: string): boolean {
        return this.firewallForm.get(controlName)?.status === "PENDING";
    }

    /**
     * Returns list of firewall types to be used in the dropdown menu.
     */
    fetchFirewallPlatforms(): void {
        this.firewallPlatforms$ = this.firewallService.fetchFirewallPlatforms();
    }

    /**
     * Handles the form submission event. It validates the form, logs the form value and validity,
     * submits the new firewall to the FirewallService, handles the server's response, and navigates
     * the user back to the firewall list upon successful creation.
     */
    onSubmit() {
        if (this.firewallForm.valid) {
            const firewall: Firewall = this.firewallForm.value as Firewall;
            this.firewallService.createFirewall(firewall).subscribe({
                next: (response) => {
                    // console.log("New firewall created:", response);
                    this.resetForm();
                    this.router.navigate(["/inventory/firewall/"]);
                },
                error: (error) => {
                    console.error("Error creating firewall:", error);
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
        this.firewallForm.reset();
    }

    /**
     * Handles the form cancellation event and navigates the user back to the firewall list.
     */
    onCancel(): void {
        this.router.navigate(["/inventory/firewall/"]);
    }
}
