import {
    ButtonGroupModule,
    ButtonModule,
    CardModule,
    CollapseModule,
    DropdownModule,
    FormModule,
    GridModule,
    NavModule,
    NavbarModule,
    SharedModule,
    UtilitiesModule,
} from "@coreui/angular";

import { ButtonGroupsComponent } from "./button-groups/button-groups.component";
import { ButtonsComponent } from "./buttons/buttons.component";
import { ButtonsRoutingModule } from "./buttons-routing.module";
import { CommonModule } from "@angular/common";
import { DropdownsComponent } from "./dropdowns/dropdowns.component";
import { IconModule } from "@coreui/icons-angular";
import { NgModule } from "@angular/core";
import { ReactiveFormsModule } from "@angular/forms";

@NgModule({
    declarations: [ButtonsComponent, ButtonGroupsComponent, DropdownsComponent],
    imports: [
        CommonModule,
        ButtonsRoutingModule,
        ButtonModule,
        ButtonGroupModule,
        GridModule,
        IconModule,
        CardModule,
        UtilitiesModule,
        DropdownModule,
        SharedModule,
        FormModule,
        ReactiveFormsModule,
        NavbarModule,
        CollapseModule,
        NavModule,
        NavbarModule,
    ],
})
export class ButtonsModule {}
