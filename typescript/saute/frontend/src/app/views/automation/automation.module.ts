import {
    AccordionModule,
    ButtonGroupModule,
    ButtonModule,
    CardModule,
    DropdownModule,
    FormModule,
    GridModule,
    ListGroupModule,
    ModalModule,
    ProgressModule,
    SharedModule,
    SpinnerModule,
} from "@coreui/angular";
import { FormsModule, ReactiveFormsModule } from "@angular/forms";

// local components
import { AdminReportComponent } from "./assessment/admin-report/admin-report.component";
import { AssuranceArpComponent } from "./operations/assurance-arp/assurance-arp.component";
import { AssuranceReadinessComponent } from "./operations/assurance-readiness/assurance-readiness.component";
import { AssuranceSnapshotComponent } from "./operations/assurance-snapshot/assurance-snapshot.component";
import { AutomationInterfaceModule } from "../../shared/modules/automation-interface/automation-interface.module";
// routing
import { AutomationRoutingModule } from "./automation-routing.module";
import { CommonModule } from "@angular/common";
import { NgModule } from "@angular/core";
import { NotificationsModule } from "../../views/notifications/notifications.module";
import { PanToPrismaComponent } from "./configuration/pan-to-prisma/pan-to-prisma.component";
import { VmseriesToAwsComponent } from "./deploy/vmseries-to-aws/vmseries-to-aws.component";
import { VmseriesToAzureComponent } from "./deploy/vmseries-to-azure/vmseries-to-azure.component";
import { VmseriesToVcenterComponent } from "./deploy/vmseries-to-vcenter/vmseries-to-vcenter.component";
import { WidgetsModule } from "../../shared/modules/widgets/widgets.module";

@NgModule({
    declarations: [
        VmseriesToAzureComponent,
        VmseriesToAwsComponent,
        VmseriesToVcenterComponent,
        PanToPrismaComponent,
        AdminReportComponent,
        AssuranceArpComponent,
        AssuranceReadinessComponent,
        AssuranceSnapshotComponent,
    ],
    imports: [
        CommonModule,
        FormsModule,
        CommonModule,
        ReactiveFormsModule,
        GridModule,
        ButtonGroupModule,
        ButtonModule,
        CardModule,
        DropdownModule,
        ListGroupModule,
        SharedModule,
        FormModule,
        AutomationRoutingModule,
        AutomationInterfaceModule,
        NotificationsModule,
        WidgetsModule,
        AccordionModule,
        ModalModule,
        SpinnerModule,
        ProgressModule,
    ],
})
export class AutomationModule {}
