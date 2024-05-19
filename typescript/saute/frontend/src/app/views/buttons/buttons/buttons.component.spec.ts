import { ButtonModule, CardModule, GridModule } from "@coreui/angular";
import { ComponentFixture, TestBed } from "@angular/core/testing";

import { ButtonsComponent } from "./buttons.component";
import { IconModule } from "@coreui/icons-angular";
import { IconSetService } from "@coreui/icons-angular";
import { RouterTestingModule } from "@angular/router/testing";
import { iconSubset } from "../../../shared/icons/icon-subset";

describe("ButtonsComponent", () => {
    let component: ButtonsComponent;
    let fixture: ComponentFixture<ButtonsComponent>;
    let iconSetService: IconSetService;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            declarations: [ButtonsComponent],
            imports: [
                CardModule,
                GridModule,
                ButtonModule,
                RouterTestingModule,
                IconModule,
            ],
            providers: [IconSetService],
        }).compileComponents();
    });

    beforeEach(() => {
        iconSetService = TestBed.inject(IconSetService);
        iconSetService.icons = { ...iconSubset };

        fixture = TestBed.createComponent(ButtonsComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it("should create", () => {
        expect(component).toBeTruthy();
    });
});
