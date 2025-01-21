import { RouterModule, Routes } from "@angular/router";

import { NgModule } from "@angular/core";
import { PrismaCreateComponent } from "./prisma-create/prisma-create.component";
import { PrismaDetailsComponent } from "./prisma-details/prisma-details.component";
import { PrismaListComponent } from "./prisma-list/prisma-list.component";

const routes: Routes = [
    {
        path: "",
        component: PrismaListComponent,
    },
    {
        path: "create",
        component: PrismaCreateComponent,
    },
    {
        path: "details/:id",
        component: PrismaDetailsComponent,
    },
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule],
})
export class PrismaRoutingModule {}
