import {
    BadgeModule,
    ButtonModule,
    CardModule,
    GridModule,
    UtilitiesModule,
} from "@coreui/angular";
import { ComponentFixture, TestBed } from "@angular/core/testing";

import { BadgesComponent } from "./badges.component";
import { IconSetService } from "@coreui/icons-angular";
import { RouterTestingModule } from "@angular/router/testing";
import { iconSubset } from "../../../shared/icons/icon-subset";

describe("BadgesComponent", () => {
    let component: BadgesComponent;
    let fixture: ComponentFixture<BadgesComponent>;
    let iconSetService: IconSetService;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            declarations: [BadgesComponent],
            imports: [
                BadgeModule,
                CardModule,
                GridModule,
                UtilitiesModule,
                ButtonModule,
                RouterTestingModule,
            ],
            providers: [IconSetService],
        }).compileComponents();
    });

    beforeEach(() => {
        iconSetService = TestBed.inject(IconSetService);
        iconSetService.icons = { ...iconSubset };

        fixture = TestBed.createComponent(BadgesComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it("should create", () => {
        expect(component).toBeTruthy();
    });
});
