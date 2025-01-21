import { Toast, ToastService } from "../../../../shared/services/toast.service";

import { Component } from "@angular/core";

@Component({
    selector: "app-toast-simple",
    template: `
        <c-toaster>
            <c-toast
                *ngFor="let toast of toasts$ | async"
                [color]="toast.color"
                [autohide]="toast.autohide"
                [delay]="toast.delay"
                [visible]="true"
                (hidden)="toastService.remove(toast)"
            >
                <c-toast-header [closeButton]="toast.closeButton">
                    {{ toast.title }}
                </c-toast-header>
                <c-toast-body
                    [innerHTML]="toast.message | safeHtml"
                ></c-toast-body>
            </c-toast>
        </c-toaster>
    `,
})
export class AppToastComponent {
    toasts$ = this.toastService.toasts$;

    constructor(public toastService: ToastService) {}
}
