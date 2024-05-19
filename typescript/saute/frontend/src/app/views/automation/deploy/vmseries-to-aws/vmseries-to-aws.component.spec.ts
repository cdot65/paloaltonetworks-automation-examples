import { ComponentFixture, TestBed } from "@angular/core/testing";

import { VmseriesToAwsComponent } from "./vmseries-to-aws.component";

describe("VmseriesToAwsComponent", () => {
    let component: VmseriesToAwsComponent;
    let fixture: ComponentFixture<VmseriesToAwsComponent>;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            declarations: [VmseriesToAwsComponent],
        }).compileComponents();

        fixture = TestBed.createComponent(VmseriesToAwsComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it("should create", () => {
        expect(component).toBeTruthy();
    });
});
