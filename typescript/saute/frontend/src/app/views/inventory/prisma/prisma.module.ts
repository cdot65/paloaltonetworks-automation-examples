import {
    ButtonGroupModule,
    ButtonModule,
    CardModule,
    DropdownModule,
    FormModule,
    GridModule,
    ListGroupModule,
    SharedModule,
} from "@coreui/angular";
import { FormsModule, ReactiveFormsModule } from "@angular/forms";

import { CommonModule } from "@angular/common";
import { NgModule } from "@angular/core";
import { PrismaCreateComponent } from "./prisma-create/prisma-create.component";
import { PrismaDetailsComponent } from "./prisma-details/prisma-details.component";
import { PrismaListComponent } from "./prisma-list/prisma-list.component";
import { PrismaRoutingModule } from "./prisma-routing.module";

@NgModule({
    declarations: [
        PrismaCreateComponent,
        PrismaListComponent,
        PrismaDetailsComponent,
    ],
    imports: [
        CommonModule,
        FormsModule,
        ReactiveFormsModule,
        GridModule,
        ButtonGroupModule,
        ButtonModule,
        CardModule,
        DropdownModule,
        ListGroupModule,
        SharedModule,
        FormModule,
        PrismaRoutingModule,
    ],
})
export class PrismaModule {}
