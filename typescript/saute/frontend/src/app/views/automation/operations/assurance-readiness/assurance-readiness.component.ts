/**
 * @file assurance-snapshot.component.ts
 *
 * This file imports the necessary Angular modules, services, and constants
 * required for the AssuranceSnapshotComponent.
 *
 * - `ChangeDetectorRef`: Utility for triggering Angular's change detection
 * - `Component`: Angular's core decorator to define a component
 * - `OnDestroy`: Lifecycle hook that gets called when this component is destroyed
 * - `OnInit`: Lifecycle hook that gets called after data-bound properties are initialized
 * - `FormBuilder`: Angular's utility for building reactive forms
 * - `FormGroup`: Interface that represents a group of form controls
 * - `Validators`: Angular's utility for form validations
 * - `Subscription`: Represents a disposable resource for an Observable execution
 * - `interval`: Observable that emits numbers in sequence on a specified interval
 * - `AutomationService`: Custom service for automation tasks
 * - `FirewallService`: Custom service for firewall-related operations
 * - `JobsService`: Custom service for job-related operations
 * - `ARP_ASSURANCE_SCRIPT`: Constant that holds the help script
 * - `ToastService`: Custom service for showing toast notifications
 * - `catchError`: RxJS operator for error handling
 * - `of`: RxJS operator to convert arguments to an observable sequence
 * - `switchMap`: RxJS operator to map each value to an observable and flatten it
 */
import { ChangeDetectorRef, Component, OnDestroy, OnInit } from "@angular/core";
import { FormBuilder, FormGroup, Validators } from "@angular/forms";
import { Subscription, interval } from "rxjs";

import { ARP_ASSURANCE_SCRIPT } from "../../../../shared/constants/arp-assurance-help";
import { AutomationService } from "../../../../shared/services/automation.service";
import { FirewallService } from "../../../../shared/services/firewall.service";
import { JobsService } from "../../../../shared/services/jobs.service";
import { ToastService } from "../../../../shared/services/toast.service";
import { catchError } from "rxjs/operators";
import { of } from "rxjs";
import { switchMap } from "rxjs/operators";

/**
 * `AssuranceReadinessComponent` serves as the main interface for the ARP Assurance feature.
 * It allows users to select a firewall and execute an ARP assurance task.
 */
@Component({
    selector: "app-assurance-readiness",
    templateUrl: "./assurance-readiness.component.html",
    styleUrls: ["./assurance-readiness.component.scss"],
})

/**
 * AssuranceReadinessComponent is an Angular component for executing an ARP Assurance Task.
 *
 * @property {string} buttonTextFirewall - Button text for the firewall selection.
 * @property {any[]} firewalls - Array containing firewall data.
 * @property {string} help - Help text generated from a constant, formatted for HTML display.
 * @property {boolean} isLoading - Indicator for whether a loading operation is in progress.
 * @property {boolean} isReportVisible - Indicator for whether the report section is visible.
 * @property {any} jobDetails - Object containing details of the job being processed.
 * @property {Subscription | undefined} jobPollingSubscription - Subscription object for job status polling.
 * @property {string} jobUrl - URL to access the details of the job.
 * @property {string} jsonData - JSON data returned from the job.
 * @property {string} jsonDataHighlighted - JSON data that is highlighted.
 * @property {any} parsedJsonData - Parsed JSON data for manipulation.
 * @property {number} progressValue - Numeric value indicating the progress of a task.
 * @property {FormGroup | any} arpAssuranceForm - FormGroup instance for handling the ARP assurance form.
 */
export class AssuranceReadinessComponent implements OnInit, OnDestroy {
    buttonTextFirewall: string = "Select Firewall";
    arpAssuranceForm: FormGroup | any;
    firewalls: any[] = [];
    help = ARP_ASSURANCE_SCRIPT.replace(/\n/g, "<br/>").replace(/ /g, "&nbsp;");
    isLoading: boolean = false;
    isReportVisible: boolean = false;
    jobDetails: any;
    jobPollingSubscription: Subscription | undefined;
    jobUrl: string = "";
    jsonData: string = "";
    jsonDataHighlighted: string = "";
    parsedJsonData: any;
    result: string = "";
    progressValue: number = 0;

    /**
     * Constructs an instance of the AssuranceSnapshotComponent.
     *
     * @param {FormBuilder} fb - Angular form builder for creating form controls and groups.
     * @param {AutomationService} AutomationService - Service for handling automation-related API calls.
     * @param {ToastService} toastService - Service for displaying toast notifications.
     * @param {ChangeDetectorRef} cdr - Angular service for triggering change detection.
     * @param {FirewallService} firewallService - Service for handling firewall-related API calls.
     * @param {JobsService} jobsService - Service for handling job-related API calls.
     */
    constructor(
        private fb: FormBuilder,
        private AutomationService: AutomationService,
        private toastService: ToastService,
        private cdr: ChangeDetectorRef,
        private firewallService: FirewallService,
        private jobsService: JobsService
    ) {}

    /**
     * Lifecycle hook that is called after data-bound properties of a directive are initialized.
     */
    ngOnInit(): void {
        this.initializeForm();
        this.fetchFirewallData();
    }

    /**
     * Initializes the arpAssuranceForm with default values and validators.
     * Sets up the structure of the form.
     */
    private initializeForm(): void {
        this.arpAssuranceForm = this.fb.group({
            ipAddress: ["", Validators.required],
            hostname: ["", Validators.required],
        });
    }

    /**
     * Fetches the list of available firewalls from the backend API.
     * If an error occurs during the fetch, logs the error and defaults the firewalls array to an empty list.
     */
    private fetchFirewallData(): void {
        this.firewallService
            .fetchFirewallData()
            .pipe(
                catchError((error) => {
                    console.error("Error fetching firewalls:", error);
                    return of([]);
                })
            )
            .subscribe((firewalls: any[]) => {
                this.firewalls = firewalls;
            });
    }

    /**
     * Lifecycle hook that is called when the component is destroyed.
     * Unsubscribes from jobPollingSubscription to prevent memory leaks.
     */
    ngOnDestroy(): void {
        if (this.jobPollingSubscription) {
            this.jobPollingSubscription.unsubscribe();
        }
    }

    /**
     * Updates the selected firewall in the arpAssuranceForm and sets the button text.
     *
     * This method is triggered when a user selects a firewall from the dropdown list.
     * It updates the 'hostname' field in the arpAssuranceForm to the selected firewall's hostname.
     * Additionally, it updates the display text of the firewall selection button to the hostname of the selected firewall.
     *
     * @param {any} selectedFirewall - The selected firewall object containing its properties, including its hostname.
     */
    selectFirewall(selectedFirewall: any): void {
        this.arpAssuranceForm
            .get("hostname")
            .setValue(selectedFirewall.hostname);
        this.buttonTextFirewall = selectedFirewall.hostname;
    }

    /**
     * Checks the validity of the arpAssuranceForm.
     *
     * This method verifies that a firewall is selected (`hostname` is not empty)
     * and at least one option within `buttonSnapshotGroup` is selected (checked).
     *
     * @returns {boolean} - Returns true if the form is valid, otherwise false.
     */
    isFormValid(): boolean {
        const formValues = this.arpAssuranceForm.value;
        const isFirewallSelected = !!formValues.hostname;

        // Regular expression to validate an IPv4 address
        const ipv4Pattern =
            /^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$/;

        // Regular expression to validate an IPv6 address
        const ipv6Pattern =
            /^(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|::1|::|:)$/;

        const isValidIpAddress =
            ipv4Pattern.test(formValues.ipAddress) ||
            ipv6Pattern.test(formValues.ipAddress);

        return isFirewallSelected && isValidIpAddress;
    }

    /**
     * Handles the form submission for ARP Assurance tasks.
     *
     * This method performs the following operations:
     * - Validates the form input.
     * - Constructs the payload required for creating an ARP Assurance task.
     * - Calls the `createArpAssuranceTask` service method to initiate the task.
     * - Displays a toast notification to indicate task submission status.
     * - Initiates polling to monitor the job status.
     * - Updates the job details and progress bar as the job progresses.
     * - Stops polling when the job is completed and displays the job details.
     *
     * @returns {void} Nothing
     */
    onSubmit(): void {
        if (this.arpAssuranceForm.valid) {
            this.isLoading = true;

            const formValues = this.arpAssuranceForm.value;

            // Prepare the payload
            const payload = {
                hostname: formValues.hostname,
                config: { ip: this.arpAssuranceForm.value.ipAddress },
            };

            this.AutomationService.createArpAssuranceTask(payload).subscribe({
                next: (response) => {
                    // console.log(response);
                    const jobId = response.task_id; // capture the job ID from the response
                    const taskUrl = `#/jobs/details/${jobId}`;
                    const anchor = `<a href="${taskUrl}" target="_blank" class="toast-link">Job Details</a>`;
                    const toast = {
                        title: "ARP Assurance task submitted successfully",
                        message: `${response.ipAddress}. ${anchor}`,
                        color: "secondary",
                        autohide: true,
                        delay: 2500,
                        closeButton: true,
                    };
                    this.toastService.show(toast);
                    this.progressValue = 10;

                    // Poll for job updates every 5 seconds
                    this.jobPollingSubscription = interval(5000)
                        .pipe(
                            switchMap(() =>
                                this.jobsService.getJobDetails(jobId)
                            )
                        )
                        .subscribe({
                            next: (jobDetails) => {
                                // Update the job details
                                this.jobDetails = jobDetails;
                                this.progressValue = 35;
                                this.isReportVisible = true;

                                // If the job is done (i.e., json_data is present), stop polling and update code editor
                                if (jobDetails.json_data) {
                                    this.jobPollingSubscription?.unsubscribe();
                                    this.cdr.detectChanges();
                                    this.jsonData = jobDetails.json_data;
                                    this.jsonData = JSON.stringify(
                                        jobDetails.json_data
                                    );
                                    this.parsedJsonData = JSON.parse(
                                        this.jsonData
                                    );
                                    this.jobUrl = taskUrl;
                                    this.progressValue = 100;
                                    this.isLoading = false;
                                }
                            },
                            error: (error) => {
                                console.error(
                                    "Error while polling job updates:",
                                    error
                                );
                            },
                        });
                },
                error: (error) => {
                    console.error(error);
                    const toast = {
                        title: "Error",
                        message: "There was an error submitting the request",
                        color: "danger",
                        autohide: true,
                        delay: 5000,
                        closeButton: true,
                    };
                    this.toastService.show(toast);
                },
            });
        } else {
            console.log("Form is not valid");
        }
    }
}
