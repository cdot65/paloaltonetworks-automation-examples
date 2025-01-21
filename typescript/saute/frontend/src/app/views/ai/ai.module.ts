import {
    AccordionModule,
    BadgeModule,
    ButtonGroupModule,
    ButtonModule,
    CardModule,
    DropdownModule,
    FormModule,
    GridModule,
    HeaderModule,
    ModalModule,
    NavModule,
    SharedModule,
    SpinnerModule,
    TableModule,
    TabsModule,
} from "@coreui/angular";

import { AiRoutingModule } from "./ai-routing.module";
import { ChangeAnalysisComponent } from "./change-analysis/change-analysis.component";
import { ChatComponent } from "./chat/chat.component";
import { CommonModule } from "@angular/common";
import { CreateScriptComponent } from "./create-script/create-script.component";
import { FormsModule } from "@angular/forms";
import { IconModule } from "@coreui/icons-angular";
import { NgModule } from "@angular/core";
import { PersonasComponent } from "./personas/personas.component";
import { ProgressModule } from "@coreui/angular";
import { ReactiveFormsModule } from "@angular/forms";
import { WidgetsModule } from "../../shared/modules/widgets/widgets.module";

@NgModule({
    declarations: [
        ChangeAnalysisComponent,
        CreateScriptComponent,
        ChatComponent,
        PersonasComponent,
    ],
    imports: [
        CommonModule,
        AiRoutingModule,
        GridModule,
        CardModule,
        FormsModule,
        HeaderModule,
        IconModule,
        ButtonModule,
        ButtonGroupModule,
        DropdownModule,
        BadgeModule,
        FormModule,
        ProgressModule,
        ReactiveFormsModule,
        SharedModule,
        AccordionModule,
        SpinnerModule,
        ModalModule,
        WidgetsModule,
        NavModule,
        TableModule,
        TabsModule,
    ],
})
export class AiModule {}
