import {
    CardModule,
    GridModule,
    NavModule,
    TabsModule,
    UtilitiesModule,
} from "@coreui/angular";
import { ColorsComponent, ThemeColorComponent } from "./colors.component";

import { CommonModule } from "@angular/common";
import { IconModule } from "@coreui/icons-angular";
import { NgModule } from "@angular/core";
// Theme Routing
import { ThemeRoutingModule } from "./theme-routing.module";
import { TypographyComponent } from "./typography.component";

@NgModule({
    imports: [
        CommonModule,
        ThemeRoutingModule,
        CardModule,
        GridModule,
        UtilitiesModule,
        IconModule,
        NavModule,
        TabsModule,
    ],
    declarations: [ColorsComponent, ThemeColorComponent, TypographyComponent],
})
export class ThemeModule {}
