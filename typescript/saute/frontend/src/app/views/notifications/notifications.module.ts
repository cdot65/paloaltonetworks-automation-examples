import {
    AlertModule,
    BadgeModule,
    ButtonModule,
    CardModule,
    FormModule,
    GridModule,
    ModalModule,
    PopoverModule,
    ProgressModule,
    SharedModule,
    ToastModule,
    TooltipModule,
    UtilitiesModule,
} from "@coreui/angular";

import { AlertsComponent } from "./alerts/alerts.component";
import { AppToastComponent } from "./toasters/toast-simple/toast.component";
import { BadgesComponent } from "./badges/badges.component";
import { CommonModule } from "@angular/common";
import { IconModule } from "@coreui/icons-angular";
import { ModalsComponent } from "./modals/modals.component";
import { NgModule } from "@angular/core";
import { NotificationsRoutingModule } from "./notifications-routing.module";
import { ReactiveFormsModule } from "@angular/forms";
import { SafeHtmlPipe } from "../../shared/pipes/safe-html.pipe";
import { ToastersComponent } from "./toasters/toasters.component";

@NgModule({
    declarations: [
        BadgesComponent,
        AlertsComponent,
        ModalsComponent,
        ToastersComponent,
        AppToastComponent,
        SafeHtmlPipe,
    ],
    imports: [
        CommonModule,
        ReactiveFormsModule,
        NotificationsRoutingModule,
        AlertModule,
        GridModule,
        CardModule,
        BadgeModule,
        ButtonModule,
        FormModule,
        ModalModule,
        ToastModule,
        SharedModule,
        UtilitiesModule,
        TooltipModule,
        PopoverModule,
        ProgressModule,
        IconModule,
    ],
    exports: [AppToastComponent],
})
export class NotificationsModule {}
