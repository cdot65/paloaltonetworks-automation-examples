import { Component } from "@angular/core";
import { HERBERT } from "../../../constants/personas/herbert";
import { JAMIE } from "../../../constants/personas/jamie";
import { Router } from "@angular/router";
import { WidgetDataService } from "../../../services/widget-data.service";

@Component({
    selector: "app-persona-widget",
    templateUrl: "./persona.component.html",
    styleUrls: ["./persona.component.scss"],
})
export class PersonaWidgetComponent {
    personaPersonas = [HERBERT, JAMIE];

    constructor(
        private widgetDataService: WidgetDataService,
        private router: Router
    ) {}

    widgetClick(widget: any) {
        // console.log("widgetClick called with widget: ", widget);
        this.widgetDataService.changeData(widget);
        this.router.navigate([widget.buttonLink]);
    }
}
