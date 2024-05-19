import { INavData } from "@coreui/angular";

export const navItems: INavData[] = [
    {
        name: "Dashboard",
        url: "/dashboard",
        iconComponent: { name: "cil-applications" },
        badge: {
            color: "info",
            text: "NEW",
        },
    },
    {
        name: "AI",
        url: "/ai",
        iconComponent: { name: "cib-react" },
        children: [
            {
                name: "Automation Mentors",
                url: "/ai/automation-mentors",
            },
            {
                name: "Change Analysis",
                // badge: {
                //   color: "danger",
                //   text: "NEW",
                // },
                url: "/ai/change-analysis",
            },
            {
                name: "Create Script",
                url: "/ai/create-script",
            },
        ],
    },
    {
        name: "Inventory",
        url: "/inventory",
        iconComponent: { name: "cil-lan" },
        children: [
            {
                name: "Firewalls",
                url: "/inventory/firewall",
            },
            {
                name: "Panorama",
                url: "/inventory/panorama",
            },
            {
                name: "Prisma",
                url: "/inventory/prisma",
            },
        ],
    },
    {
        name: "Jobs",
        url: "/jobs",
        iconComponent: { name: "cil-list" },
    },
];
