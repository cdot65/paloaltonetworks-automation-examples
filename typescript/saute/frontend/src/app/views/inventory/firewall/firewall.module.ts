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
import { FirewallCreateComponent } from "./firewall-create/firewall-create.component";
import { FirewallDetailsComponent } from "./firewall-details/firewall-details.component";
import { FirewallListComponent } from "./firewall-list/firewall-list.component";
import { FirewallRoutingModule } from "./firewall-routing.module";
import { NgModule } from "@angular/core";

@NgModule({
    declarations: [
        FirewallCreateComponent,
        FirewallListComponent,
        FirewallDetailsComponent,
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
        FirewallRoutingModule,
    ],
})
export class FirewallModule {}
