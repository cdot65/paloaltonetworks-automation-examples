import { RouterModule, Routes } from "@angular/router";

import { AlertsComponent } from "./alerts/alerts.component";
import { BadgesComponent } from "./badges/badges.component";
import { ModalsComponent } from "./modals/modals.component";
import { NgModule } from "@angular/core";
import { ToastersComponent } from "./toasters/toasters.component";

const routes: Routes = [
    {
        path: "",
        data: {
            title: "Notifications",
        },
        children: [
            {
                path: "",
                pathMatch: "full",
                redirectTo: "badges",
            },
            {
                path: "alerts",
                component: AlertsComponent,
                data: {
                    title: "Alerts",
                },
            },
            {
                path: "badges",
                component: BadgesComponent,
                data: {
                    title: "Badges",
                },
            },
            {
                path: "modal",
                component: ModalsComponent,
                data: {
                    title: "Modal",
                },
            },
            {
                path: "toasts",
                component: ToastersComponent,
                data: {
                    title: "Toasts",
                },
            },
        ],
    },
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule],
})
export class NotificationsRoutingModule {}
