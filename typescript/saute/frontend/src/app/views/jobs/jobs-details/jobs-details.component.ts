import { ChangeDetectorRef, Component, OnDestroy, OnInit } from "@angular/core";
import { Subscription, of, timer } from "rxjs";
import { catchError, switchMap } from "rxjs/operators";

import { ActivatedRoute } from "@angular/router";
import { JobsService } from "../../../shared/services/jobs.service";
import { Params } from "@angular/router";
import { Router } from "@angular/router";

@Component({
    selector: "app-jobs-details",
    templateUrl: "./jobs-details.component.html",
})
export class JobsDetailsComponent implements OnInit, OnDestroy {
    data: any;
    isJobCompleted: boolean = false;
    private pollingSubscription: Subscription = new Subscription();

    constructor(
        private route: ActivatedRoute,
        private router: Router,
        private jobsService: JobsService,
        private cdr: ChangeDetectorRef
    ) {}

    ngOnInit(): void {
        this.route.params
            .pipe(
                switchMap((params: Params) => {
                    const taskId = params["id"];
                    return this.jobsService.getJobDetails(taskId);
                })
            )
            .subscribe((job: any) => {
                if (job !== null) {
                    this.data = job;
                    if (job.json_data) {
                        this.isJobCompleted = true;
                        this.stopPolling();
                    }
                    this.cdr.detectChanges();
                }
            });
    }

    ngOnDestroy(): void {
        this.stopPolling();
    }

    startPolling(taskId: string) {
        const pollingInterval = 5000;

        this.pollingSubscription = timer(0, pollingInterval)
            .pipe(switchMap(() => this.jobsService.getJobDetails(taskId)))
            .subscribe((job: any) => {
                if (job !== null) {
                    this.data = job;
                    if (job.json_data) {
                        this.isJobCompleted = true;
                        this.stopPolling();
                    }
                    this.cdr.detectChanges();
                }
            });
    }

    stopPolling() {
        if (this.pollingSubscription) {
            this.pollingSubscription.unsubscribe();
        }
    }

    close(): void {
        this.router.navigate(["/inventory/jobs"]);
    }
}
