import { ButtonModule, ProgressModule, ToastModule } from "@coreui/angular";
import { ComponentFixture, TestBed, waitForAsync } from "@angular/core/testing";

import { AppToastComponent } from "./toast.component";
import { IconSetService } from "@coreui/icons-angular";
import { NoopAnimationsModule } from "@angular/platform-browser/animations";
import { iconSubset } from "../../../../shared/icons/icon-subset";

describe("ToastComponent", () => {
    let component: AppToastComponent;
    let fixture: ComponentFixture<AppToastComponent>;
    let iconSetService: IconSetService;

    beforeEach(waitForAsync(() => {
        TestBed.configureTestingModule({
            declarations: [AppToastComponent],
            imports: [
                NoopAnimationsModule,
                ToastModule,
                ProgressModule,
                ButtonModule,
            ],
            providers: [IconSetService],
        }).compileComponents();
    }));

    beforeEach(() => {
        iconSetService = TestBed.inject(IconSetService);
        iconSetService.icons = { ...iconSubset };

        fixture = TestBed.createComponent(AppToastComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it("should create", () => {
        expect(component).toBeTruthy();
    });
});
