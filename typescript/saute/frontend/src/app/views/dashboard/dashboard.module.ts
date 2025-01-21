import {
    AvatarModule,
    BadgeModule,
    ButtonGroupModule,
    ButtonModule,
    CardModule,
    FormModule,
    GridModule,
    NavModule,
    ProgressModule,
    TableModule,
    TabsModule,
} from "@coreui/angular";

import { ChartjsModule } from "@coreui/angular-chartjs";
import { CommonModule } from "@angular/common";
import { DashboardComponent } from "./dashboard.component";
import { DashboardRoutingModule } from "./dashboard-routing.module";
import { IconModule } from "@coreui/icons-angular";
import { NgModule } from "@angular/core";
import { ReactiveFormsModule } from "@angular/forms";
import { WidgetsModule } from "../../shared/modules/widgets/widgets.module";

@NgModule({
    imports: [
        DashboardRoutingModule,
        CardModule,
        NavModule,
        IconModule,
        TabsModule,
        CommonModule,
        GridModule,
        ProgressModule,
        ReactiveFormsModule,
        ButtonModule,
        FormModule,
        ButtonModule,
        ButtonGroupModule,
        ChartjsModule,
        AvatarModule,
        TableModule,
        WidgetsModule,
    ],
    declarations: [DashboardComponent],
})
export class DashboardModule {}
