import {
    ButtonGroupModule,
    ButtonModule,
    CardModule,
    CollapseModule,
    DropdownModule,
    GridModule,
    NavModule,
    NavbarModule,
} from "@coreui/angular";
import { ComponentFixture, TestBed } from "@angular/core/testing";

import { DropdownsComponent } from "./dropdowns.component";
import { IconSetService } from "@coreui/icons-angular";
import { NoopAnimationsModule } from "@angular/platform-browser/animations";
import { RouterTestingModule } from "@angular/router/testing";
import { iconSubset } from "../../../shared/icons/icon-subset";

describe("DropdownsComponent", () => {
    let component: DropdownsComponent;
    let fixture: ComponentFixture<DropdownsComponent>;
    let iconSetService: IconSetService;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            declarations: [DropdownsComponent],
            imports: [
                ButtonModule,
                DropdownModule,
                CollapseModule,
                NoopAnimationsModule,
                GridModule,
                CardModule,
                RouterTestingModule,
                NavModule,
                NavbarModule,
                ButtonGroupModule,
            ],
            providers: [IconSetService],
        }).compileComponents();
    });

    beforeEach(() => {
        iconSetService = TestBed.inject(IconSetService);
        iconSetService.icons = { ...iconSubset };

        fixture = TestBed.createComponent(DropdownsComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it("should create", () => {
        expect(component).toBeTruthy();
    });
});
