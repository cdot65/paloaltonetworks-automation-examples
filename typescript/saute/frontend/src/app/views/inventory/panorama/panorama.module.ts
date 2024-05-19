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
import { PanoramaCreateComponent } from "./panorama-create/panorama-create.component";
import { PanoramaDetailsComponent } from "./panorama-details/panorama-details.component";
import { PanoramaListComponent } from "./panorama-list/panorama-list.component";
import { PanoramaRoutingModule } from "./panorama-routing.module";

@NgModule({
    declarations: [
        PanoramaCreateComponent,
        PanoramaListComponent,
        PanoramaDetailsComponent,
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
        PanoramaRoutingModule,
    ],
})
export class PanoramaModule {}
