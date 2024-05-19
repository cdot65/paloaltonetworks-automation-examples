import {
    ButtonModule,
    CardModule,
    DropdownModule,
    GridModule,
    ProgressModule,
    SharedModule,
    WidgetModule,
} from "@coreui/angular";

import { AutomationAssessmentComponent } from "./assessment/assessment.component";
import { AutomationConfigurationComponent } from "./configuration/configuration.component";
import { AutomationDeployComponent } from "./deploy/deploy.component";
import { AutomationOperationsComponent } from "./operations/operations.component";
import { ChartjsModule } from "@coreui/angular-chartjs";
import { CodeEditorModule } from "@ngstack/code-editor";
import { CodeEditorWidgetComponent } from "./code-editor/code-editor.component";
import { CommonModule } from "@angular/common";
import { IconModule } from "@coreui/icons-angular";
import { NgModule } from "@angular/core";
import { PersonaWidgetComponent } from "./persona/persona.component";
import { WidgetsRoutingModule } from "./widgets-routing.module";

@NgModule({
    declarations: [
        AutomationDeployComponent,
        AutomationConfigurationComponent,
        AutomationOperationsComponent,
        AutomationAssessmentComponent,
        PersonaWidgetComponent,
        CodeEditorWidgetComponent,
    ],
    imports: [
        CommonModule,
        WidgetsRoutingModule,
        GridModule,
        WidgetModule,
        IconModule,
        DropdownModule,
        SharedModule,
        ButtonModule,
        CardModule,
        ProgressModule,
        ChartjsModule,
        CodeEditorModule.forRoot(),
    ],
    exports: [
        AutomationDeployComponent,
        AutomationConfigurationComponent,
        AutomationOperationsComponent,
        AutomationAssessmentComponent,
        PersonaWidgetComponent,
        CodeEditorWidgetComponent,
    ],
})
export class WidgetsModule {}
