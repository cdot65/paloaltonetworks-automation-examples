import { ComponentFixture, TestBed } from "@angular/core/testing";
import { FormsModule } from "@angular/forms";
import { RouterTestingModule } from "@angular/router/testing";

import {
  ButtonModule,
  CardModule,
  FormModule,
  GridModule,
  ListGroupModule,
} from "@coreui/angular";
import { IconSetService } from "@coreui/icons-angular";
import { iconSubset } from "../../../shared/icons/icon-subset";
import { ValidationComponent } from "./validation.component";

describe("ValidationComponent", () => {
  let component: ValidationComponent;
  let fixture: ComponentFixture<ValidationComponent>;
  let iconSetService: IconSetService;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ValidationComponent],
      imports: [
        FormModule,
        ButtonModule,
        ListGroupModule,
        FormsModule,
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

    fixture = TestBed.createComponent(ValidationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it("should create", () => {
    expect(component).toBeTruthy();
  });
});
