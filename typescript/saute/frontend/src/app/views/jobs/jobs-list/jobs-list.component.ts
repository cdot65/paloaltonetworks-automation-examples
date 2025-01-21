import { Component, OnInit } from "@angular/core";
import { HttpClient, HttpHeaders } from "@angular/common/http";

import { JobsService } from "../../../shared/services/jobs.service";
import { Router } from "@angular/router";
import Swal from "sweetalert2";
import { catchError } from "rxjs/operators";
import { of } from "rxjs";

@Component({
    selector: "app-jobs-list",
    templateUrl: "./jobs-list.component.html",
})
export class JobsListComponent implements OnInit {
    jobsData: any[] = [];
    searchTerm: string = "";
    currentPage: number = 1;
    pageSize: number = 15;
    pageSizeOptions: number[] = [15, 50, 100];

    constructor(
        private http: HttpClient,
        private router: Router,
        private jobsService: JobsService
    ) {}

    ngOnInit(): void {
        this.fetchJobsData();
    }

    fetchJobsData() {
        this.jobsService.fetchJobsData().subscribe((data: any[]) => {
            this.jobsData = data;
        });
    }

    applyFilter(event: Event) {
        const filterValue = (event.target as HTMLInputElement).value;
        this.searchTerm = filterValue.trim().toLowerCase();
    }

    sortData(property: string) {
        this.jobsData = this.jobsData.sort((a, b) => {
            if (a[property] < b[property]) {
                return -1;
            }
            if (a[property] > b[property]) {
                return 1;
            }
            return 0;
        });
    }

    changePage(page: number) {
        this.currentPage = page;
    }

    changePageSize(size: number) {
        this.pageSize = size;
        this.currentPage = 1;
    }

    shouldDisplayJob(job: any): boolean {
        const searchMatch = JSON.stringify(job)
            .toLowerCase()
            .includes(this.searchTerm);
        const index = this.jobsData.indexOf(job);
        return (
            searchMatch &&
            index >= (this.currentPage - 1) * this.pageSize &&
            index < this.currentPage * this.pageSize
        );
    }

    ceil(value: number): number {
        return Math.ceil(value);
    }
}
