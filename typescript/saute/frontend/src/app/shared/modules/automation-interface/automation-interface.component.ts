import {
    AfterContentInit,
    AfterViewInit,
    ChangeDetectionStrategy,
    ChangeDetectorRef,
    Component,
    Input,
    OnInit,
} from "@angular/core";

import { CodeModel } from "@ngstack/code-editor";
import { ScriptService } from "src/app/shared/services/script.service";
import packageJson from "../../../../../package.json";

@Component({
    selector: "app-automation-interface",
    templateUrl: "./automation-interface.component.html",
    styleUrls: ["./automation-interface.component.scss"],
    changeDetection: ChangeDetectionStrategy.OnPush,
})
export class AutomationInterfaceComponent
    implements OnInit, AfterContentInit, AfterViewInit
{
    @Input() scriptName: string = "";
    activeTab: string = "execute";

    theme = "vs-dark";
    readOnly = false;
    codeModel!: CodeModel;
    options: any = {
        contextmenu: true,
        lineNumbers: true,
        minimap: {
            enabled: true,
        },
    };

    constructor(
        private changeDetectorRef: ChangeDetectorRef,
        private scriptService: ScriptService
    ) {}

    ngOnInit(): void {
        if (this.scriptName) {
            this.fetchScriptContent();
        }
    }

    ngAfterContentInit(): void {
        this.changeDetectorRef.detectChanges();
    }

    ngAfterViewInit(): void {
        this.changeDetectorRef.markForCheck();
    }

    fetchScriptContent(): void {
        if (this.scriptName) {
            this.scriptService.fetchScriptByName(this.scriptName).subscribe({
                next: (data) => {
                    if (data?.file_content) {
                        this.codeModel = {
                            language: "python",
                            uri: "main.py",
                            value: data.file_content,
                        };
                        this.changeDetectorRef.detectChanges();
                    }
                },
                error: (error) => console.error(error),
            });
        }
    }

    onCodeChanged(value: string) {
        console.log(value);
    }
}
