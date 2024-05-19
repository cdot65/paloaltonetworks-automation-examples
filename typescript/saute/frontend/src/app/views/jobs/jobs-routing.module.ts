import { RouterModule, Routes } from "@angular/router";

import { JobsDetailsComponent } from "./jobs-details/jobs-details.component";
import { JobsListComponent } from "./jobs-list/jobs-list.component";
import { NgModule } from "@angular/core";

const routes: Routes = [
    {
        path: "",
        component: JobsListComponent,
    },
    {
        path: "details/:id",
        component: JobsDetailsComponent,
    },
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule],
})
export class JobsRoutingModule {}
