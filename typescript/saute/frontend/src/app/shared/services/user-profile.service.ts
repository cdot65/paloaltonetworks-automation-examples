import { BehaviorSubject } from "rxjs";
import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { environment } from "../../../environments/environment.prod";

@Injectable({
    providedIn: "root",
})
export class UserProfileService {
    private API_URL = environment.apiUrl;
    private apiUrl = environment.apiUrl;
    private userProfileUrl = environment.apiUrl + "/api/v1/user-profile/";
    private profileImageUrlSubject = new BehaviorSubject<string | null>(null);

    constructor(private http: HttpClient) {}

    getProfileImageUrl() {
        return this.profileImageUrlSubject.asObservable();
    }

    updateProfileImageUrl() {
        this.http.get<any>(this.userProfileUrl).subscribe({
            next: (profile) => {
                const fullImageUrl = this.apiUrl + profile.profile_image;
                this.profileImageUrlSubject.next(fullImageUrl);
            },
            error: (error) => {
                console.error("Error fetching user profile", error);
            },
        });
    }
}
