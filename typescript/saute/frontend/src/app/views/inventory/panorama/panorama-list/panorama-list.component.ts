/**
 * PanoramaListComponent handles fetching, displaying, and managing the
 * list of ingredients in the inventory.
 */
import { Component, OnInit } from "@angular/core";

import { Panorama } from "../../../../shared/interfaces/panorama.interface";
import { PanoramaService } from "../../../../shared/services/panorama.service";
import { Router } from "@angular/router";

@Component({
    selector: "app-panorama-list",
    templateUrl: "./panorama-list.component.html",
})

/**
 * PanoramaListComponent is an Angular component for displaying and managing
 * the list of ingredients in the inventory.
 */
export class PanoramaListComponent implements OnInit {
    // Array to store the fetched panorama data
    panoramaData: Panorama[];
    detailsVisible: { [key: string]: boolean } = {};

    /**
     * Constructor for the PanoramaListComponent; injects required
     * services and initializes the ingredientData array.
     */
    constructor(
        private panoramaService: PanoramaService,
        private router: Router
    ) {
        this.panoramaData = [];
    }

    // Angular lifecycle hook that initializes the component
    ngOnInit() {
        this.fetchPanoramaData();
    }

    /**
     * Fetches the panorama data from the PanoramaService and
     * stores it in the ingredientData array.
     */

    fetchPanoramaData() {
        this.panoramaService
            .panoramaInventory()
            .subscribe((data: Panorama[]) => {
                this.panoramaData = data;
            });
    }

    /**
     * Deletes an existing panorama entry based on the provided UUID.
     *
     * @param uuid - The UUID of the panorama entry to delete
     */
    deleteEntry(uuid: string): void {
        this.panoramaService.deleteEntry(uuid).subscribe(() => {
            this.fetchPanoramaData();
        });
    }

    /**
     * Navigates to the "/inventory/panorama/create" route when the user clicks
     * the "Create New Recipe" button.
     */
    navigateToCreate(): void {
        this.router.navigate(["/inventory/panorama/create"]);
    }

    /**
     * Navigates to the "/inventory/panorama/details" route with the provided UUID
     * when the user clicks the "Edit" button.
     *
     * @param uuid - UUID of the panorama entry to edit
     */
    navigateToDetails(uuid: string): void {
        this.router.navigate(["/inventory/panorama/details", uuid]);
    }

    /**
     * Toggle the row to reveal edit and delete buttons.
     *
     * @param uuid - UUID of the panorama entry to edit
     */
    toggleDetails(uuid: string): void {
        this.detailsVisible[uuid] = !this.detailsVisible[uuid];
    }
}
