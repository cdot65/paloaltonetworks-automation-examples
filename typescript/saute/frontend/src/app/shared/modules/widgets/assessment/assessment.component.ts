import { Component } from "@angular/core";

@Component({
    selector: "app-assessment-widget",
    templateUrl: "./assessment.component.html",
    styleUrls: ["./assessment.component.scss"],
})
export class AutomationAssessmentComponent {
    assessmentData = [
        {
            imagePath: "../../../../../assets/img/brand/python-panos.svg",
            title: "Security Policy Lookup Tool",
            description:
                "Enter your parameters and find out if a security policy already exists on Panorama.",
            buttonLink: "/deploy",
            hashtags: ["#panos", "#python"],
        },
        {
            imagePath: "../../../../../assets/img/brand/python-panos.svg",
            title: "Admin Report",
            description:
                "Send an email report that represents a list of configured Panorama Administrators",
            buttonLink: "/automation/assessment/admin-report",
            hashtags: ["#panorama", "#python", "#email"],
        },
        {
            imagePath: "../../../../../assets/img/brand/python-panos.svg",
            title: "BPA Report (PAN-OS)",
            description:
                "Create a new Best Practices Analysis for a PAN-OS firewall.",
            buttonLink: "/deploy",
            hashtags: ["#panos", "#python"],
        },
        {
            imagePath: "../../../../../assets/img/brand/python-panos.svg",
            title: "BPA Report (Panorama)",
            description:
                "Create a new Best Practices Analysis for a Panorama appliance.",
            buttonLink: "/deploy",
            hashtags: ["#panos", "#python"],
        },
    ];
}
