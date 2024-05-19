import {
    ButtonModule,
    CardModule,
    FormModule,
    GridModule,
} from "@coreui/angular";
import { ComponentFixture, TestBed } from "@angular/core/testing";

import { IconModule } from "@coreui/icons-angular";
import { IconSetService } from "@coreui/icons-angular";
import { RegisterComponent } from "./register.component";
import { iconSubset } from "../../../shared/icons/icon-subset";

describe("RegisterComponent", () => {
    let component: RegisterComponent;
    let fixture: ComponentFixture<RegisterComponent>;
    let iconSetService: IconSetService;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            declarations: [RegisterComponent],
            imports: [
                CardModule,
                FormModule,
                GridModule,
                ButtonModule,
                IconModule,
            ],
            providers: [IconSetService],
        }).compileComponents();
    });

    beforeEach(() => {
        iconSetService = TestBed.inject(IconSetService);
        iconSetService.icons = { ...iconSubset };

        fixture = TestBed.createComponent(RegisterComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it("should create", () => {
        expect(component).toBeTruthy();
    });
});
