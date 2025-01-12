// frontend/src/app/pages/edl/edl.routes.ts
import { Routes } from '@angular/router';
import { EdlList } from './edl-list/edl-list';
import { EdlDetails } from './edl-details/edl-details';

export default [
    { path: '', component: EdlList },
    { path: ':name', component: EdlDetails },
    { path: '**', redirectTo: '' }
] as Routes;
