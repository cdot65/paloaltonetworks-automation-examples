import { ChangeDetectorRef, Component, OnDestroy, OnInit } from "@angular/core";
import {
    ChatWithBot,
    ResponseModel,
} from "../../../shared/models/gpt-response";
import { ElementRef, ViewChild } from "@angular/core";
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { cilArrowRight, cilChartPie } from "@coreui/icons";

import { BotResponseService } from "../../../shared/services/chat.service";
import { CookieService } from "ngx-cookie-service";
import { Router } from "@angular/router";
import { Subscription } from "rxjs";
import { WidgetDataService } from "../../../shared/services/widget-data.service";
import { environment } from "../../../../environments/environment.prod";
import { map } from "rxjs/operators";

@Component({
    selector: "app-chat",
    templateUrl: "./chat.component.html",
    styleUrls: ["./chat.component.scss"],
})
export class ChatComponent implements OnInit, OnDestroy {
    @ViewChild("chatBox") private chatContainer!: ElementRef;
    private API_URL = environment.apiUrl;
    authorId: string = ""; // to store author's id
    chatConversation: ChatWithBot[] = []; // Array to hold chat conversation
    icons = { cilChartPie, cilArrowRight };
    promptText = ""; // Text entered by the user
    response!: ResponseModel | undefined; // Response from GPT-4
    selectedWidget: any; // Currently selected widget
    showTyping = false; // Boolean to show typing animation
    messagePollingSubscription: Subscription | undefined;
    lastMessageIndex: number | undefined; // initialize it as undefined
    conversationId: string = this.generateUUID(); // Initialize with a UUID
    selectedModel: string = "gpt-4"; // Initialize with gpt-4

    constructor(
        private widgetDataService: WidgetDataService,
        private router: Router,
        private botResponseService: BotResponseService,
        private http: HttpClient,
        private cookieService: CookieService,
        private cdr: ChangeDetectorRef
    ) {}

    ngOnInit(): void {
        // Check if there is any widget data
        this.widgetDataService.currentData.subscribe((data) => {
            if (data && Object.keys(data).length !== 0) {
                this.selectedWidget = data;
                localStorage.setItem("widgetData", JSON.stringify(data)); // save data to local storage
            } else {
                let savedData = localStorage.getItem("widgetData"); // retrieve saved data
                if (savedData) {
                    this.selectedWidget = JSON.parse(savedData);
                } else {
                    this.router.navigate(["/dashboard"]);
                }
            }
        });

        // get user data
        this.getUserData();

        // Generate a UUID for this conversation when the component is loaded
        this.conversationId = this.generateUUID();
    }

    ngOnDestroy(): void {
        if (this.messagePollingSubscription) {
            this.messagePollingSubscription.unsubscribe();
        }
    }

    ngAfterViewChecked() {
        this.scrollToBottom();
    }

    scrollToBottom(): void {
        try {
            this.chatContainer.nativeElement.scrollTop =
                this.chatContainer.nativeElement.scrollHeight;
        } catch (err) {}
    }

    sendChatMessage() {
        this.llmMessage(this.selectedModel, this.promptText, "You", "person");
        // console.log("promptText:", this.promptText);
        this.messageToLlm();
    }

    llmMessage(
        model: string,
        content: string,
        person: string,
        cssClass: string
    ) {
        const chatToPush: ChatWithBot = {
            model: model,
            person: person,
            response: content,
            cssClass: cssClass,
        };
        this.chatConversation.push(chatToPush);
    }

    getText(data: string) {
        return data.split("\n").filter((f) => f.length > 0);
    }

    generateUUID(): string {
        return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(
            /[xy]/g,
            function (c) {
                let r = (Math.random() * 16) | 0,
                    v = c === "x" ? r : (r & 0x3) | 0x8;
                return v.toString(16);
            }
        );
    }

    getUserData() {
        const authToken = this.cookieService.get("auth_token");
        const headers = new HttpHeaders().set(
            "Authorization",
            `Token ${authToken}`
        );

        this.http
            .get(`${this.API_URL}/api/v1/dj-rest-auth/user/`, {
                headers,
            })
            .pipe(map((response) => response as any)) // map response to any
            .subscribe({
                next: (response) => {
                    this.authorId = response.pk;
                },
                error: (error) => {
                    console.error("Error getting user data:", error);
                },
            });
    }

    messageToLlm() {
        if (this.promptText.length < 2) return;

        try {
            this.response = undefined;
            this.showTyping = true;

            // Adjusting the payload as per backend expectation
            const backendPayload = {
                message: this.promptText,
                conversation_id: this.conversationId,
                llm: this.selectedModel,
                persona: this.selectedWidget.name,
                author_id: this.authorId,
            };

            this.botResponseService.generateResponse(backendPayload).subscribe({
                next: (response) => {
                    // Start/Restart the polling here
                    this.pollMessages(backendPayload.conversation_id);
                },
                error: (error) => {
                    this.showTyping = false;
                    console.error(
                        `Error with OpenAI API request: ${error.message}`
                    );
                },
            });
        } catch (error: any) {
            this.showTyping = false;

            if (error.response) {
                console.error(error.response.status, error.response.data);
            } else {
                console.error(
                    `Error with OpenAI API request: ${error.message}`
                );
            }
        }
    }

    pollMessages(conversationId: string) {
        // console.log("pollMessages called with conversationId:", conversationId);

        // Unsubscribe the previous polling if it exists
        if (this.messagePollingSubscription) {
            this.messagePollingSubscription.unsubscribe();
        }

        this.messagePollingSubscription = this.botResponseService
            .pollBotResponses(conversationId)
            .subscribe((response: any) => {
                const newMessage = response;

                if (
                    !this.lastMessageIndex ||
                    newMessage.index > this.lastMessageIndex
                ) {
                    this.lastMessageIndex = newMessage.index;

                    if (newMessage.content.trim() != "") {
                        // to make sure the message is not empty
                        this.showTyping = false; // stop showing the typing animation
                        this.llmMessage(
                            "llm",
                            newMessage.content,
                            this.selectedWidget.name,
                            "bot"
                        );
                        this.cdr.detectChanges();
                        if (this.messagePollingSubscription) {
                            this.messagePollingSubscription.unsubscribe(); // stop polling after receiving the message
                        }
                    }
                }
            });
    }
}
