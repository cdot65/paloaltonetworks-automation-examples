import { RouterModule, Routes } from "@angular/router";

// AuthGuard
import { AuthGuard } from "./auth.guard";
import { DefaultLayoutComponent } from "./containers";
import { LoginComponent } from "./views/pages/login/login.component";
import { NgModule } from "@angular/core";
import { Page404Component } from "./views/pages/page404/page404.component";
import { Page500Component } from "./views/pages/page500/page500.component";
import { RegisterComponent } from "./views/pages/register/register.component";

const routes: Routes = [
    {
        path: "",
        redirectTo: "dashboard",
        pathMatch: "full",
    },
    {
        path: "",
        component: DefaultLayoutComponent,
        data: {
            title: "Home",
        },
        children: [
            {
                path: "dashboard",
                loadChildren: () =>
                    import("./views/dashboard/dashboard.module").then(
                        (m) => m.DashboardModule
                    ),
                canActivate: [AuthGuard],
            },
            {
                path: "widgets",
                loadChildren: () =>
                    import("./shared/modules/widgets/widgets.module").then(
                        (m) => m.WidgetsModule
                    ),
                canActivate: [AuthGuard],
            },
            {
                path: "pages",
                loadChildren: () =>
                    import("./views/pages/pages.module").then(
                        (m) => m.PagesModule
                    ),
                canActivate: [AuthGuard],
            },
            {
                path: "inventory/firewall",
                loadChildren: () =>
                    import("./views/inventory/firewall/firewall.module").then(
                        (m) => m.FirewallModule
                    ),
                canActivate: [AuthGuard],
            },
            {
                path: "inventory/panorama",
                loadChildren: () =>
                    import("./views/inventory/panorama/panorama.module").then(
                        (m) => m.PanoramaModule
                    ),
                canActivate: [AuthGuard],
            },
            {
                path: "inventory/prisma",
                loadChildren: () =>
                    import("./views/inventory/prisma/prisma.module").then(
                        (m) => m.PrismaModule
                    ),
                canActivate: [AuthGuard],
            },
            {
                path: "jobs",
                loadChildren: () =>
                    import("./views/jobs/jobs.module").then(
                        (m) => m.JobsModule
                    ),
                canActivate: [AuthGuard],
            },
            {
                path: "automation",
                loadChildren: () =>
                    import("./views/automation/automation.module").then(
                        (m) => m.AutomationModule
                    ),
                canActivate: [AuthGuard],
            },
            {
                path: "ai",
                loadChildren: () =>
                    import("./views/ai/ai.module").then((m) => m.AiModule),
                canActivate: [AuthGuard],
            },
            {
                path: "script",
                loadChildren: () =>
                    import(
                        "./shared/modules/automation-interface/automation-interface.module"
                    ).then((m) => m.AutomationInterfaceModule),
                canActivate: [AuthGuard],
            },
        ],
    },
    {
        path: "404",
        component: Page404Component,
        data: {
            title: "Page 404",
        },
    },
    {
        path: "500",
        component: Page500Component,
        data: {
            title: "Page 500",
        },
    },
    {
        path: "login",
        component: LoginComponent,
        data: {
            title: "Login Page",
        },
    },
    {
        path: "register",
        component: RegisterComponent,
        data: {
            title: "Register Page",
        },
    },
    { path: "**", redirectTo: "dashboard" },
];

@NgModule({
    imports: [
        RouterModule.forRoot(routes, {
            scrollPositionRestoration: "top",
            anchorScrolling: "enabled",
            initialNavigation: "enabledBlocking",
            // relativeLinkResolution: 'legacy'
        }),
    ],
    exports: [RouterModule],
})
export class AppRoutingModule {}
