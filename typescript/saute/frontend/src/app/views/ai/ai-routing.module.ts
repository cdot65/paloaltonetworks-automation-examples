import { RouterModule, Routes } from "@angular/router";

import { ChangeAnalysisComponent } from "./change-analysis/change-analysis.component";
import { ChatComponent } from "./chat/chat.component";
import { CreateScriptComponent } from "./create-script/create-script.component";
import { NgModule } from "@angular/core";
import { PersonasComponent } from "./personas/personas.component";

const routes: Routes = [
    {
        path: "",
        data: {
            title: "AI",
        },
        children: [
            {
                path: "",
                redirectTo: "create-script",
                pathMatch: "full",
            },
            {
                path: "automation-mentors",
                component: PersonasComponent,
                data: {
                    title: "Automation Mentors",
                },
            },
            {
                path: "change-analysis",
                component: ChangeAnalysisComponent,
                data: {
                    title: "change-analysis",
                },
            },
            {
                path: "chat",
                component: ChatComponent,
                data: {
                    title: "Chat",
                },
            },
            {
                path: "create-script",
                component: CreateScriptComponent,
                data: {
                    title: "create-script",
                },
            },
            {
                path: "**",
                redirectTo: "history",
            },
        ],
    },
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule],
})
export class AiRoutingModule {}
