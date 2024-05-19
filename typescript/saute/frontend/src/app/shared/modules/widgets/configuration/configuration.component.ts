import { Component } from "@angular/core";

@Component({
    selector: "app-configuration-widget",
    templateUrl: "./configuration.component.html",
    styleUrls: ["./configuration.component.scss"],
})
export class AutomationConfigurationComponent {
    configurationData = [
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
            title: "New Address Object",
            description: "Create a new address object on Panorama appliances.",
            buttonLink: "/deploy",
            hashtags: ["#panos", "#python"],
        },
        {
            imagePath: "../../../../../assets/img/brand/python-panos.svg",
            title: "New Address Group",
            description:
                "Create a new address group object on Panorama appliances.",
            buttonLink: "/deploy",
            hashtags: ["#panos", "#python"],
        },
        {
            imagePath: "../../../../../assets/img/brand/python-panos.svg",
            title: "New Security Rule",
            description:
                "Use Python to create a new address object on PAN-OS firewalls.",
            buttonLink: "/deploy",
            hashtags: ["#panos", "#python"],
        },
        {
            imagePath: "../../../../../assets/img/brand/python-prisma.svg",
            title: "New Remote Network on Prisma Access",
            description:
                "Use Python to create a new remote network configuration on Prisma Access.",
            buttonLink: "/deploy",
            hashtags: ["#prisma", "#python"],
        },
        {
            imagePath:
                "../../../../../assets/img/brand/python-panos-prisma.svg",
            title: "Sync Panorama with Prisma Access",
            description:
                "Use Python to sync Panorama configuration to Prisma Access.",
            buttonLink: "/automation/configuration/pan-to-prisma",
            hashtags: ["#panos", "#prisma", "#python"],
        },
    ];
}
