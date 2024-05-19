/**
 * FirewallListComponent handles fetching, displaying, and managing the
 * list of ingredients in the inventory.
 */
import { Component, OnInit } from "@angular/core";

import { Firewall } from "../../../../shared/interfaces/firewall.interface";
import { FirewallService } from "../../../../shared/services/firewall.service";
import { Router } from "@angular/router";

@Component({
    selector: "app-firewall-list",
    templateUrl: "./firewall-list.component.html",
})

/**
 * FirewallListComponent is an Angular component for displaying and managing
 * the list of ingredients in the inventory.
 */
export class FirewallListComponent implements OnInit {
    // Array to store the fetched firewall data
    firewallData: Firewall[];
    detailsVisible: { [key: string]: boolean } = {};

    /**
     * Constructor for the FirewallListComponent; injects required
     * services and initializes the ingredientData array.
     */
    constructor(
        private firewallService: FirewallService,
        private router: Router
    ) {
        this.firewallData = [];
    }

    // Angular lifecycle hook that initializes the component
    ngOnInit() {
        this.fetchFirewallData();
    }

    /**
     * Fetches the firewall data from the FirewallService and
     * stores it in the ingredientData array.
     */

    fetchFirewallData() {
        this.firewallService
            .fetchFirewallData()
            .subscribe((data: Firewall[]) => {
                this.firewallData = data;
            });
    }

    /**
     * Deletes an existing firewall entry based on the provided UUID.
     *
     * @param uuid - The UUID of the firewall entry to delete
     */
    deleteEntry(uuid: string): void {
        this.firewallService.deleteEntry(uuid).subscribe(() => {
            this.fetchFirewallData();
        });
    }

    /**
     * Navigates to the "/inventory/firewall/create" route when the user clicks
     * the "Create New Recipe" button.
     */
    navigateToCreate(): void {
        this.router.navigate(["/inventory/firewall/create"]);
    }

    /**
     * Navigates to the "/inventory/firewall/details" route with the provided UUID
     * when the user clicks the "Edit" button.
     *
     * @param uuid - UUID of the firewall entry to edit
     */
    navigateToDetails(uuid: string): void {
        this.router.navigate(["/inventory/firewall/details", uuid]);
    }

    /**
     * Toggle the row to reveal edit and delete buttons.
     *
     * @param uuid - UUID of the firewall entry to edit
     */
    toggleDetails(uuid: string): void {
        this.detailsVisible[uuid] = !this.detailsVisible[uuid];
    }
}
