import { ComponentFixture, TestBed } from "@angular/core/testing";

import { VmseriesToAzureComponent } from "./vmseries-to-azure.component";

describe("VmseriesToAzureComponent", () => {
    let component: VmseriesToAzureComponent;
    let fixture: ComponentFixture<VmseriesToAzureComponent>;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            declarations: [VmseriesToAzureComponent],
        }).compileComponents();

        fixture = TestBed.createComponent(VmseriesToAzureComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it("should create", () => {
        expect(component).toBeTruthy();
    });
});
