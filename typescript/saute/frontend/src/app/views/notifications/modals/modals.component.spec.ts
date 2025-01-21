import {
    ButtonModule,
    CardModule,
    GridModule,
    ModalModule,
    PopoverModule,
    TooltipModule,
} from "@coreui/angular";
import { ComponentFixture, TestBed } from "@angular/core/testing";

import { IconSetService } from "@coreui/icons-angular";
import { ModalsComponent } from "./modals.component";
import { NoopAnimationsModule } from "@angular/platform-browser/animations";
import { RouterTestingModule } from "@angular/router/testing";
import { iconSubset } from "../../../shared/icons/icon-subset";

describe("ModalsComponent", () => {
    let component: ModalsComponent;
    let fixture: ComponentFixture<ModalsComponent>;
    let iconSetService: IconSetService;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            declarations: [ModalsComponent],
            imports: [
                ModalModule,
                NoopAnimationsModule,
                GridModule,
                CardModule,
                PopoverModule,
                ButtonModule,
                RouterTestingModule,
                TooltipModule,
            ],
            providers: [IconSetService],
        }).compileComponents();
    });

    beforeEach(() => {
        iconSetService = TestBed.inject(IconSetService);
        iconSetService.icons = { ...iconSubset };

        fixture = TestBed.createComponent(ModalsComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it("should create", () => {
        expect(component).toBeTruthy();
    });
});
