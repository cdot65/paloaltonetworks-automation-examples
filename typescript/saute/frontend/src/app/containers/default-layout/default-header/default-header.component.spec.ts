import {
    AvatarModule,
    BadgeModule,
    BreadcrumbModule,
    DropdownModule,
    GridModule,
    HeaderModule,
    NavModule,
    SidebarModule,
} from "@coreui/angular";
import { ComponentFixture, TestBed } from "@angular/core/testing";

import { DefaultHeaderComponent } from "./default-header.component";
import { IconSetService } from "@coreui/icons-angular";
import { RouterTestingModule } from "@angular/router/testing";
import { iconSubset } from "../../../shared/icons/icon-subset";

describe("DefaultHeaderComponent", () => {
    let component: DefaultHeaderComponent;
    let fixture: ComponentFixture<DefaultHeaderComponent>;
    let iconSetService: IconSetService;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            declarations: [DefaultHeaderComponent],
            imports: [
                GridModule,
                HeaderModule,
                NavModule,
                BadgeModule,
                AvatarModule,
                DropdownModule,
                BreadcrumbModule,
                RouterTestingModule,
                SidebarModule,
            ],
            providers: [IconSetService],
        }).compileComponents();
    });

    beforeEach(() => {
        iconSetService = TestBed.inject(IconSetService);
        iconSetService.icons = { ...iconSubset };

        fixture = TestBed.createComponent(DefaultHeaderComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it("should create", () => {
        expect(component).toBeTruthy();
    });
});
