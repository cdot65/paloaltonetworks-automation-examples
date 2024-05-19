import {
    ButtonModule,
    CardModule,
    FormModule,
    GridModule,
    ProgressModule,
    ToastModule,
} from "@coreui/angular";
import { ComponentFixture, TestBed, waitForAsync } from "@angular/core/testing";
import { FormsModule, ReactiveFormsModule } from "@angular/forms";

import { AppToastComponent } from "./toast-simple/toast.component";
import { IconSetService } from "@coreui/icons-angular";
import { NoopAnimationsModule } from "@angular/platform-browser/animations";
import { ToastersComponent } from "./toasters.component";
import { iconSubset } from "../../../shared/icons/icon-subset";

describe("ToastersComponent", () => {
    let component: ToastersComponent;
    let fixture: ComponentFixture<ToastersComponent>;
    let iconSetService: IconSetService;

    beforeEach(waitForAsync(() => {
        TestBed.configureTestingModule({
            declarations: [ToastersComponent, AppToastComponent],
            imports: [
                NoopAnimationsModule,
                GridModule,
                ToastModule,
                CardModule,
                FormModule,
                ButtonModule,
                ProgressModule,
                FormsModule,
                ReactiveFormsModule,
            ],
            providers: [IconSetService],
        }).compileComponents();
    }));

    beforeEach(() => {
        iconSetService = TestBed.inject(IconSetService);
        iconSetService.icons = { ...iconSubset };

        fixture = TestBed.createComponent(ToastersComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it("should create", () => {
        expect(component).toBeTruthy();
    });
});
