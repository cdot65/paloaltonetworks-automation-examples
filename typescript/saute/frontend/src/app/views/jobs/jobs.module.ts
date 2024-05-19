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
import { JobsDetailsComponent } from "./jobs-details/jobs-details.component";
import { JobsListComponent } from "./jobs-list/jobs-list.component";
import { JobsRoutingModule } from "./jobs-routing.module";
import { NgModule } from "@angular/core";

@NgModule({
    declarations: [JobsListComponent, JobsDetailsComponent],
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
        JobsRoutingModule,
    ],
})
export class JobsModule {}
