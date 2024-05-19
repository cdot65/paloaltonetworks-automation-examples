import { ClassToggleService, HeaderComponent } from "@coreui/angular";
import { Component, Input } from "@angular/core";
import { FormControl, FormGroup } from "@angular/forms";

import { AuthService } from "../../../auth.service";
import { UserProfileService } from "../../../shared/services/user-profile.service";

@Component({
    selector: "app-default-header",
    templateUrl: "./default-header.component.html",
})
export class DefaultHeaderComponent extends HeaderComponent {
    @Input() sidebarId: string = "sidebar";

    public newMessages = new Array(4);
    public newTasks = new Array(5);
    public newNotifications = new Array(5);
    public profileImageUrl: string | null = null;

    constructor(
        private classToggler: ClassToggleService,
        private authService: AuthService,
        private userProfileService: UserProfileService
    ) {
        super();
        this.updateProfileImageUrl();
    }

    updateProfileImageUrl(): void {
        this.userProfileService.getProfileImageUrl().subscribe({
            next: (url) => {
                this.profileImageUrl = url;
            },
            error: (error) => {
                console.error("Error fetching user profile image URL", error);
            },
        });
    }

    onLogoutClick(): void {
        this.authService.logout();
    }
}
