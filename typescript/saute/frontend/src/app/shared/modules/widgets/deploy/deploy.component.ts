import { Component } from "@angular/core";

@Component({
    selector: "app-deploy-widget",
    templateUrl: "./deploy.component.html",
    styleUrls: ["./deploy.component.scss"],
})
export class AutomationDeployComponent {
    deployData = [
        {
            imagePath:
                "../../../../../assets/img/brand/terraform-panos-aws.svg",
            title: "Deploy VM-Series to AWS",
            description: "Deploy VM-Series on Amazon Web Services",
            buttonLink: "/upload",
            hashtags: ["#aws", "#terraform", "#vm-series"],
        },
        {
            imagePath:
                "../../../../../assets/img/brand/terraform-panos-azure.svg",
            title: "Deploy VM-Series to Azure",
            description: "Deploy VM-Series on Microsoft Azure",
            buttonLink: "/upload",
            hashtags: ["#azure", "#terraform", "#vm-series"],
        },
        {
            imagePath:
                "../../../../../assets/img/brand/terraform-panos-gcp.svg",
            title: "Deploy VM-Series to GCP",
            description: "Deploy VM-Series on Google Compute Platform",
            capBg: { "--cui-card-cap-bg": "#FF9900" },
            values: [{ title: "Deploy", value: "Now" }],
            buttonLink: "/deploy",
            hashtags: ["#aws", "#terraform", "#vm-series"],
        },
        {
            imagePath:
                "../../../../../assets/img/brand/terraform-panos-vsphere.svg",
            title: "Deploy VM-Series to vCenter",
            description: "Deploy VM-Series on vSphere",
            buttonLink: "/automation/operations/get-software-information",
            hashtags: ["#vcenter", "#terraform", "#vm-series"],
        },
        {
            imagePath:
                "../../../../../assets/img/brand/terraform-panos-proxmox.svg",
            title: "Deploy VM-Series to Proxmox",
            description: "Deploy VM-Series on Proxmox",
            buttonLink: "/automation/operations/get-software-information",
            hashtags: ["#vcenter", "#terraform", "#vm-series"],
        },
    ];
}
