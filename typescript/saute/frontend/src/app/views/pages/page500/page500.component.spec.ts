import { ButtonModule, FormModule, GridModule } from "@coreui/angular";
import { ComponentFixture, TestBed } from "@angular/core/testing";

import { IconModule } from "@coreui/icons-angular";
import { IconSetService } from "@coreui/icons-angular";
import { Page500Component } from "./page500.component";
import { iconSubset } from "../../../shared/icons/icon-subset";

describe("Page500Component", () => {
    let component: Page500Component;
    let fixture: ComponentFixture<Page500Component>;
    let iconSetService: IconSetService;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            declarations: [Page500Component],
            imports: [GridModule, ButtonModule, FormModule, IconModule],
            providers: [IconSetService],
        }).compileComponents();
    });

    beforeEach(() => {
        iconSetService = TestBed.inject(IconSetService);
        iconSetService.icons = { ...iconSubset };

        fixture = TestBed.createComponent(Page500Component);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it("should create", () => {
        expect(component).toBeTruthy();
    });
});
