import { Component } from "@angular/core";

@Component({
    selector: "app-operations-widget",
    templateUrl: "./operations.component.html",
    styleUrls: ["./operations.component.scss"],
})
export class AutomationOperationsComponent {
    operationsData = [
        {
            imagePath: "../../../../../assets/img/brand/python-panos.svg",
            title: "Assurance ARP entry",
            description: "Validate if ARP entry is found on firewall.",
            buttonLink: "/automation/operations/assurance-arp",
            hashtags: ["#panos", "#assurance", "#python"],
        },
        {
            imagePath: "../../../../../assets/img/brand/python-panos.svg",
            title: "Firewall State Snapshots",
            description: "Snapshot operational data from a firewall.",
            buttonLink: "/automation/operations/assurance-snapshot",
            hashtags: ["#panos", "#assurance", "#python"],
        },
        {
            imagePath: "../../../../../assets/img/brand/python-panos.svg",
            title: "Upgrade Readiness Check",
            description:
                "Perform a series of checks to see if a PAN-OS firewall is ready to begin the upgrade process.",
            buttonLink: "/automation/operations/assurance-readiness",
            hashtags: ["#panos", "#assurance", "#python"],
        },
    ];
}
