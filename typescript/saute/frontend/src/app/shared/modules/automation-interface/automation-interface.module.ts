import {
    GridModule,
    ListGroupModule,
    NavModule,
    SharedModule,
    TabsModule,
    UtilitiesModule,
} from "@coreui/angular";

import { AutomationInterfaceComponent } from "./automation-interface.component";
import { CodeEditorModule } from "@ngstack/code-editor";
import { CommonModule } from "@angular/common";
import { IconModule } from "@coreui/icons-angular";
import { NgModule } from "@angular/core";
import { RouterModule } from "@angular/router";
import { WidgetsModule } from "../widgets/widgets.module";

@NgModule({
    declarations: [AutomationInterfaceComponent],
    exports: [AutomationInterfaceComponent],
    imports: [
        CommonModule,
        NavModule,
        IconModule,
        RouterModule,
        TabsModule,
        UtilitiesModule,
        WidgetsModule,
        GridModule,
        ListGroupModule,
        SharedModule,
        CodeEditorModule.forRoot(),
    ],
})
export class AutomationInterfaceModule {}
