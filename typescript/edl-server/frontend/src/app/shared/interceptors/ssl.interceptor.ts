// src/app/shared/interceptors/ssl.interceptor.ts
import {
    HttpHandlerFn,
    HttpInterceptorFn,
    HttpRequest,
    HttpEvent
} from '@angular/common/http';
import { Observable } from 'rxjs';
import { environmentProd } from '../../../environments/environment';

export const sslInterceptor: HttpInterceptorFn = (
    request: HttpRequest<unknown>,
    next: HttpHandlerFn
): Observable<HttpEvent<unknown>> => {
    if (environmentProd.ignoreCertificateErrors) {
        // Clone the request and add any necessary headers or configurations
        const sslRequest = request.clone({
            // specific headers or configurations here
            headers: request.headers.set('X-Ignore-SSL', 'true')
        });
        return next(sslRequest);
    }
    return next(request);
};
