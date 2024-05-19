import {
    ButtonGroupModule,
    ButtonModule,
    CardModule,
    DropdownModule,
    FormModule,
    GridModule,
} from "@coreui/angular";
import { ComponentFixture, TestBed } from "@angular/core/testing";

import { ButtonGroupsComponent } from "./button-groups.component";
import { IconSetService } from "@coreui/icons-angular";
import { ReactiveFormsModule } from "@angular/forms";
import { RouterTestingModule } from "@angular/router/testing";
import { iconSubset } from "../../../shared/icons/icon-subset";

describe("ButtonGroupsComponent", () => {
    let component: ButtonGroupsComponent;
    let fixture: ComponentFixture<ButtonGroupsComponent>;
    let iconSetService: IconSetService;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            declarations: [ButtonGroupsComponent],
            imports: [
                ReactiveFormsModule,
                ButtonModule,
                DropdownModule,
                FormModule,
                GridModule,
                CardModule,
                RouterTestingModule,
                ButtonModule,
                ButtonGroupModule,
            ],
            providers: [IconSetService],
        }).compileComponents();
    });

    beforeEach(() => {
        iconSetService = TestBed.inject(IconSetService);
        iconSetService.icons = { ...iconSubset };

        fixture = TestBed.createComponent(ButtonGroupsComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it("should create", () => {
        expect(component).toBeTruthy();
    });
});
