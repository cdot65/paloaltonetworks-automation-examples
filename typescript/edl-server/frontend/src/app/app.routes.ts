// src/app/app.routes.ts

import { Routes } from '@angular/router';
import { LayoutComponent } from './shared/components/layout/layout/layout.component';

export const APP_ROUTES: Routes = [
    {
        path: '',
        component: LayoutComponent,
        children: [
            {
                path: '',
                loadComponent: () =>
                    import(
                        './pages/components/edl-list/edl-list.component'
                        ).then((m) => m.EdlListComponent),
            },
            {
                path: 'edl',  // Add this parent path for EDL features
                children: [
                    {
                        path: '',  // This will be the list view
                        loadComponent: () =>
                            import(
                                './pages/components/edl-list/edl-list.component'
                                ).then((m) => m.EdlListComponent),
                    },
                    {
                        path: ':name',  // This will match /edl/:name
                        loadComponent: () =>
                            import(
                                './pages/components/edl-details/edl-details.component'
                                ).then((m) => m.EdlDetailsComponent),
                    }
                ]
            },
            {
                path: 'search',
                loadComponent: () =>
                    import(
                        './pages/search-results-page/search-results-page.component'
                        ).then((m) => m.SearchResultsPageComponent),
            },
        ],
    },
    {
        path: 'auth',
        children: [
            {
                path: 'login',
                loadComponent: () =>
                    import('./pages/auth/login-page/login-page.component').then(
                        (m) => m.LoginPageComponent,
                    ),
            },
            {
                path: 'register',
                loadComponent: () =>
                    import(
                        './pages/auth/register-page/register-page.component'
                    ).then((m) => m.RegisterPageComponent),
            },
        ],
    },
    {
        path: '404',
        loadComponent: () =>
            import('./pages/not-found-page/not-found-page.component').then(
                (m) => m.NotFoundPageComponent,
            ),
    },
    {
        path: '**',
        redirectTo: '/404',
    },
];
