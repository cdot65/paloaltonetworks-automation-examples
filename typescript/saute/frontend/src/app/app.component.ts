import { Component, OnInit } from "@angular/core";
import { NavigationEnd, Router } from "@angular/router";

import { IconSetService } from "@coreui/icons-angular";
import { Title } from "@angular/platform-browser";
import { iconSubset } from "./shared/icons/icon-subset";

@Component({
    selector: "app-root",
    template: `
        <app-toast-simple></app-toast-simple>
        <router-outlet></router-outlet>
    `,
})
export class AppComponent implements OnInit {
    title = "Saute";

    constructor(
        private router: Router,
        private titleService: Title,
        private iconSetService: IconSetService
    ) {
        titleService.setTitle(this.title);
        iconSetService.icons = { ...iconSubset };
    }

    ngOnInit(): void {
        this.router.events.subscribe((evt) => {
            if (!(evt instanceof NavigationEnd)) {
                return;
            }
        });
    }
}
