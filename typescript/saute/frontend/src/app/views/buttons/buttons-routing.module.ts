import { RouterModule, Routes } from "@angular/router";

import { ButtonGroupsComponent } from "./button-groups/button-groups.component";
import { ButtonsComponent } from "./buttons/buttons.component";
import { DropdownsComponent } from "./dropdowns/dropdowns.component";
import { NgModule } from "@angular/core";

const routes: Routes = [
    {
        path: "",
        data: {
            title: "Buttons",
        },
        children: [
            {
                path: "",
                pathMatch: "full",
                redirectTo: "buttons",
            },
            {
                path: "buttons",
                component: ButtonsComponent,
                data: {
                    title: "Buttons",
                },
            },
            {
                path: "button-groups",
                component: ButtonGroupsComponent,
                data: {
                    title: "Button groups",
                },
            },
            {
                path: "dropdowns",
                component: DropdownsComponent,
                data: {
                    title: "Dropdowns",
                },
            },
        ],
    },
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule],
})
export class ButtonsRoutingModule {}
