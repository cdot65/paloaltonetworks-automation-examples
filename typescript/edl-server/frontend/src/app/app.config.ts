// src/app/app.config.ts
import { ApplicationConfig } from '@angular/core';
import { provideRouter, withInMemoryScrolling } from '@angular/router';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { provideAnimations } from '@angular/platform-browser/animations';
import { APP_ROUTES } from './app.routes';
import { authInterceptor } from './shared/interceptors/auth.interceptor';
import { sslInterceptor } from './shared/interceptors/ssl.interceptor';

export const appConfig: ApplicationConfig = {
    providers: [
        // Router configuration
        provideRouter(
            APP_ROUTES,
            withInMemoryScrolling({
                scrollPositionRestoration: 'enabled',
                anchorScrolling: 'enabled',
            }),
        ),

        // HTTP configuration with interceptors
        provideHttpClient(withInterceptors([authInterceptor, sslInterceptor])),

        // Browser animations
        provideAnimations(),
    ],
};
