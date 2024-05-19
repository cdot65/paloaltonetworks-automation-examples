import {
    AlertModule,
    ButtonModule,
    CardModule,
    GridModule,
} from "@coreui/angular";
import { ComponentFixture, TestBed } from "@angular/core/testing";

import { AlertsComponent } from "./alerts.component";
import { IconSetService } from "@coreui/icons-angular";
import { NoopAnimationsModule } from "@angular/platform-browser/animations";
import { RouterTestingModule } from "@angular/router/testing";
import { iconSubset } from "../../../shared/icons/icon-subset";

describe("AlertsComponent", () => {
    let component: AlertsComponent;
    let fixture: ComponentFixture<AlertsComponent>;
    let iconSetService: IconSetService;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            declarations: [AlertsComponent],
            imports: [
                AlertModule,
                ButtonModule,
                NoopAnimationsModule,
                GridModule,
                CardModule,
                RouterTestingModule,
            ],
            providers: [IconSetService],
        }).compileComponents();
    });

    beforeEach(() => {
        iconSetService = TestBed.inject(IconSetService);
        iconSetService.icons = { ...iconSubset };

        fixture = TestBed.createComponent(AlertsComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it("should create", () => {
        expect(component).toBeTruthy();
    });
});
