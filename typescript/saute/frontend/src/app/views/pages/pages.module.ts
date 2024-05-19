import {
    ButtonModule,
    CardModule,
    FormModule,
    GridModule,
} from "@coreui/angular";

import { AuthService } from "../../auth.service";
import { CommonModule } from "@angular/common";
import { CookieService } from "ngx-cookie-service";
import { FormsModule } from "@angular/forms";
import { IconModule } from "@coreui/icons-angular";
import { LoginComponent } from "./login/login.component";
import { MatSnackBarModule } from "@angular/material/snack-bar";
import { NgModule } from "@angular/core";
import { Page404Component } from "./page404/page404.component";
import { Page500Component } from "./page500/page500.component";
import { PagesRoutingModule } from "./pages-routing.module";
import { RegisterComponent } from "./register/register.component";

@NgModule({
    declarations: [
        LoginComponent,
        RegisterComponent,
        Page404Component,
        Page500Component,
    ],
    imports: [
        CommonModule,
        PagesRoutingModule,
        CardModule,
        ButtonModule,
        GridModule,
        IconModule,
        FormModule,
        FormsModule,
        MatSnackBarModule,
    ],
    providers: [AuthService, CookieService],
})
export class PagesModule {}
