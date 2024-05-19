import { ButtonModule, FormModule, GridModule } from "@coreui/angular";
import { ComponentFixture, TestBed } from "@angular/core/testing";

import { IconModule } from "@coreui/icons-angular";
import { IconSetService } from "@coreui/icons-angular";
import { Page404Component } from "./page404.component";
import { iconSubset } from "../../../shared/icons/icon-subset";

describe("Page404Component", () => {
    let component: Page404Component;
    let fixture: ComponentFixture<Page404Component>;
    let iconSetService: IconSetService;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            declarations: [Page404Component],
            imports: [FormModule, GridModule, ButtonModule, IconModule],
            providers: [IconSetService],
        }).compileComponents();
    });

    beforeEach(() => {
        iconSetService = TestBed.inject(IconSetService);
        iconSetService.icons = { ...iconSubset };

        fixture = TestBed.createComponent(Page404Component);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it("should create", () => {
        expect(component).toBeTruthy();
    });
});
