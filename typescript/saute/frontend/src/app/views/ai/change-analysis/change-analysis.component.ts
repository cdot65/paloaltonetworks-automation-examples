import { ChangeDetectorRef, Component, OnDestroy, OnInit } from "@angular/core";
import { FormBuilder, FormGroup, Validators } from "@angular/forms";
import { Subscription, interval } from "rxjs";

import { AiService } from "../../../shared/services/ai.service";
import { CHANGE_ANALYSIS_TIPS } from "../../../shared/constants/change-analysis-tips";
import { DISCLAIMER_TEXT } from "../../../shared/constants/disclaimer";
import { DomSanitizer } from "@angular/platform-browser";
import { JobsService } from "src/app/shared/services/jobs.service";
import { ToastService } from "../../../shared/services/toast.service";
import { catchError } from "rxjs/operators";
import { of } from "rxjs";
import { switchMap } from "rxjs/operators";

@Component({
    selector: "app-change-analysis",
    templateUrl: "./change-analysis.component.html",
    styleUrls: ["./change-analysis.component.scss"],
})
export class ChangeAnalysisComponent implements OnInit, OnDestroy {
    comparisonForm: FormGroup | any;
    expertiseLevel: string = "Select Expertise Level";
    assuranceJobs: any[] = [];
    beforeSnapshot: string = "";
    afterSnapshot: string = "";
    beforeSnapshotDate: string = 'Select "Before" Snapshot';
    afterSnapshotDate: string = 'Select "After" Snapshot';
    jobDetails: any;
    jobPollingSubscription: Subscription | undefined;
    progressValue: number = 0;
    jsonData: string = "";
    jsonDataHighlighted: string = "";
    comparisonAnalysis: string = "Comparing Snapshots...";
    items = [1];
    isLoading: boolean = false;
    disclaimer = DISCLAIMER_TEXT.replace(/\n/g, "<br/>");
    chatGptTips = CHANGE_ANALYSIS_TIPS.replace(/\n/g, "<br/>");

    constructor(
        private fb: FormBuilder,
        private AiService: AiService,
        private toastService: ToastService,
        private sanitizer: DomSanitizer,
        private cdr: ChangeDetectorRef,
        private jobsService: JobsService
    ) {}

    ngOnInit(): void {
        this.comparisonForm = this.fb.group({
            message: ["", Validators.required],
            beforeSnapshot: ["", Validators.required],
            afterSnapshot: ["", Validators.required],
            expertiseLevel: ["", Validators.required],
        });
        this.fetchJobsData();
    }

    ngOnDestroy(): void {
        if (this.jobPollingSubscription) {
            this.jobPollingSubscription.unsubscribe();
        }
    }

    fetchJobsData(): void {
        this.jobsService
            .fetchJobsData()
            .pipe(
                catchError((error) => {
                    console.error("Error fetching jobs:", error);
                    return of([]);
                })
            )
            .subscribe((jobs: any[]) => {
                this.assuranceJobs = jobs.filter(
                    (job) => job.job_type === "assurance_snapshot"
                );
                // console.log(this.assuranceJobs);
            });
    }

    formatDate(dateString: string): string {
        const date = new Date(dateString);
        return date.toISOString().split(".")[0] + "Z";
    }

    selectBeforeSnapshot(job: any): void {
        this.comparisonForm.get("beforeSnapshot").setValue(job.task_id);
        this.beforeSnapshotDate = this.formatDate(job.created_at);
        // console.log(this.comparisonForm.get("beforeSnapshot").value);
    }

    selectAfterSnapshot(job: any): void {
        this.comparisonForm.get("afterSnapshot").setValue(job.task_id);
        this.afterSnapshotDate = this.formatDate(job.created_at);
        // console.log(this.comparisonForm.get("afterSnapshot").value);
    }

    selectExpertiseLevel(level: string): void {
        this.comparisonForm.get("expertiseLevel").setValue(level);
        this.expertiseLevel = level;
        // console.log(this.comparisonForm.get("expertiseLevel").value);
    }

    onSubmit(): void {
        if (this.comparisonForm.valid) {
            this.isLoading = true;

            const comparisonDetails = this.comparisonForm.value;

            // console.log(comparisonDetails);

            this.AiService.sendChangeAnalysis(comparisonDetails).subscribe({
                next: (response) => {
                    // console.log(response);
                    const jobId = response.task_id; // capture the job ID from the response
                    const taskUrl = `#/jobs/details/${jobId}`;
                    const anchor = `<a href="${taskUrl}" target="_blank" class="toast-link">Job Details</a>`;
                    const toast = {
                        title: "Comparison request submitted successfully",
                        message: `${response.message}. ${anchor}`,
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

                                // If the job is done (i.e., json_data is present), stop polling and update code editor
                                if (jobDetails.json_data) {
                                    this.jobPollingSubscription?.unsubscribe();
                                    this.cdr.detectChanges();
                                    this.jsonData = jobDetails.json_data;
                                    this.comparisonAnalysis =
                                        "Comparison Report";
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
