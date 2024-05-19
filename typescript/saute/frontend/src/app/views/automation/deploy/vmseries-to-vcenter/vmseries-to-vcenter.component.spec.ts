import { ComponentFixture, TestBed } from "@angular/core/testing";

import { VmseriesToVcenterComponent } from "./vmseries-to-vcenter.component";

describe("VmseriesToVcenterComponent", () => {
    let component: VmseriesToVcenterComponent;
    let fixture: ComponentFixture<VmseriesToVcenterComponent>;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            declarations: [VmseriesToVcenterComponent],
        }).compileComponents();

        fixture = TestBed.createComponent(VmseriesToVcenterComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it("should create", () => {
        expect(component).toBeTruthy();
    });
});
