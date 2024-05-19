import {
    Component,
    Input,
    OnChanges,
    OnInit,
    SimpleChanges,
} from "@angular/core";

import { CodeModel } from "@ngstack/code-editor";

@Component({
    selector: "app-code-editor-widget",
    templateUrl: "./code-editor.component.html",
    styleUrls: ["./code-editor.component.scss"],
})
export class CodeEditorWidgetComponent implements OnChanges, OnInit {
    @Input() codeObject: any;

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

    ngOnChanges(changes: SimpleChanges) {
        if (changes["codeObject"]) {
            if (this.codeObject) {
                console.log("CodeObject received:", this.codeObject); // Log the received codeObject
                this.codeModel = {
                    language: "python",
                    uri: "main.py",
                    value: this.codeObject,
                };
            } else {
                console.log("CodeObject received is empty or null"); // If codeObject is null or empty
            }
        }
    }

    ngOnInit(): void {
        console.log("CodeEditorWidgetComponent initialized");
    }

    onCodeChanged(value: string) {
        console.log("Code changed:", value); // Log when the code in editor changes
    }
}
