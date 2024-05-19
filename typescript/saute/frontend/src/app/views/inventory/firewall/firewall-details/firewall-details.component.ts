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
 * FirewallDetailsComponent handles displaying and updating firewall entries.
 */
import { ActivatedRoute, Router } from "@angular/router";
import { Component, OnInit } from "@angular/core";
import {
    Firewall,
    FirewallPlatform,
} from "../../../../shared/interfaces/firewall.interface";
import { debounceTime, first, map, switchMap } from "rxjs/operators";
import { distinctUntilChanged, of, timer } from "rxjs";

import { FirewallService } from "../../../../shared/services/firewall.service";
import { Observable } from "rxjs";

@Component({
    selector: "app-firewall-details",
    templateUrl: "./firewall-details.component.html",
})

/**
 * FirewallDetailsComponent is an Angular component for displaying and updating
 * an individual firewall entry based on its identifier (UUID).
 */
export class FirewallDetailsComponent implements OnInit {
    // Form group for the firewall entry form
    firewallForm!: FormGroup;
    // Unique identifier (UUID) for the firewall
    uuid!: string;
    firewallExistsErrorMessage = "";
    firewall: Firewall | undefined;
    firewallPlatforms$!: Observable<FirewallPlatform[]>;

    /**
     * Constructor for the FirewallDetailsComponent. Initializes the form group
     * and injects required services and modules.
     */
    constructor(
        private route: ActivatedRoute,
        private router: Router,
        private firewallService: FirewallService
    ) {
        this.editForm();
    }

    // Angular lifecycle hook that initializes the component
    ngOnInit(): void {
        this.firewallPlatforms$ = this.firewallService.fetchFirewallPlatforms();

        this.route.params.subscribe((params) => {
            this.uuid = params["id"];
            this.fetchFirewallData();
        });
    }

    /**
     * Initializes the firewallForm FormGroup with default form controls.
     */
    editForm(): void {
        this.firewallForm = new FormGroup({
            api_key: new FormControl(""),
            hostname: new FormControl(""),
            ipv4_address: new FormControl(""),
            ipv6_address: new FormControl(""),
            notes: new FormControl(""),
            platform: new FormControl(null),
        });
    }

    /**
     * Fetches the firewall data and sets it to the firewallForm FormGroup
     * based on the provided UUID.
     */
    fetchFirewallData(): void {
        this.firewallService
            .fetchFirewallData()
            .subscribe((data: Firewall[]) => {
                this.firewall = data.find((i) => i.uuid === this.uuid);
                if (this.firewall) {
                    this.firewallForm.setValue({
                        api_key: this.firewall.api_key,
                        hostname: this.firewall.hostname,
                        ipv4_address: this.firewall.ipv4_address,
                        ipv6_address: this.firewall.ipv6_address,
                        notes: this.firewall.notes || "",
                        platform: this.firewall.platform,
                    });
                }
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
     * Updates an existing firewall entry with the provided data.
     * Redirects to the "/inventory/firewall/" route on successful update.
     *
     * @param updatedEntry - The updated firewall data to be submitted
     */
    updateEntry(updatedEntry: Firewall): void {
        if (this.firewallForm.valid && this.uuid) {
            this.firewallService
                .updateFirewall(updatedEntry, this.uuid)
                .subscribe({
                    next: () => {
                        this.router.navigate(["/inventory/firewall/"]);
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
