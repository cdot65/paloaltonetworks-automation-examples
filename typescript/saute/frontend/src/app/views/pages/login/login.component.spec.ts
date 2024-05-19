import {
    ButtonModule,
    CardModule,
    FormModule,
    GridModule,
} from "@coreui/angular";
import { ComponentFixture, TestBed } from "@angular/core/testing";

import { IconModule } from "@coreui/icons-angular";
import { IconSetService } from "@coreui/icons-angular";
import { LoginComponent } from "./login.component";
import { iconSubset } from "../../../shared/icons/icon-subset";

describe("LoginComponent", () => {
    let component: LoginComponent;
    let fixture: ComponentFixture<LoginComponent>;
    let iconSetService: IconSetService;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            declarations: [LoginComponent],
            imports: [
                FormModule,
                CardModule,
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

        fixture = TestBed.createComponent(LoginComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it("should create", () => {
        expect(component).toBeTruthy();
    });
});
