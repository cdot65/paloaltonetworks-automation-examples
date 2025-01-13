// src/app/layout/component/app.footer.ts
import { Component } from '@angular/core';

@Component({
    standalone: true,
    selector: 'app-footer',
    template: ` <div class="layout-footer">
        Pomegranate by
        <a href="https://github.com/cdot65" target="_blank" rel="noopener noreferrer" class="text-primary font-bold hover:underline">cdot65</a>
    </div>`
})
export class AppFooter {}
