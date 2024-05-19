import { Component, OnInit } from "@angular/core";
import { Toast, ToastService } from "../../../../shared/services/toast.service";

import { NgForm } from "@angular/forms";
import { PanoramaService } from "../../../../shared/services/panorama.service";

@Component({
    selector: "app-admin-report",
    templateUrl: "./admin-report.component.html",
    styleUrls: ["./admin-report.component.scss"],
})
export class AdminReportComponent implements OnInit {
    panoramas: any[] = [];
    selectedPanorama: any = null;
    email: string = "";

    constructor(
        private panoramaService: PanoramaService,
        private toastService: ToastService
    ) {}

    ngOnInit(): void {
        this.panoramaService.panoramaInventory().subscribe((data: any[]) => {
            this.panoramas = data;
        });
    }

    onSubmitForm(form: NgForm): void {
        if (form.valid) {
            const jobDetails = {
                pan_url: this.selectedPanorama.hostname,
                api_key: this.selectedPanorama.api_key,
                to_emails: this.email,
            };

            // console.log("jobDetails:", jobDetails);

            this.panoramaService
                .executeAdminReport(jobDetails)
                .subscribe((response) => {
                    // console.log(response);
                    const taskUrl = `#/jobs/details/${response.task_id}`;
                    const anchor = `<a href="${taskUrl}" target="_blank" class="toast-link">Job Details</a>`;
                    const toast: Toast = {
                        title: "Job submitted successfully",
                        message: `${response.message}. ${anchor}`,
                        color: "secondary",
                        autohide: true,
                        delay: 5000,
                        closeButton: true,
                    };
                    this.toastService.show(toast);
                });
        } else {
            console.error("Form is invalid");
        }
    }
}
