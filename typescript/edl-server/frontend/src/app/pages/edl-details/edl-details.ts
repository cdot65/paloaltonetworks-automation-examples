import { Component, OnInit, signal, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Table, TableModule } from 'primeng/table';
import { ButtonModule } from 'primeng/button';
import { RippleModule } from 'primeng/ripple';
import { ToastModule } from 'primeng/toast';
import { ToolbarModule } from 'primeng/toolbar';
import { InputTextModule } from 'primeng/inputtext';
import { DialogModule } from 'primeng/dialog';
import { TagModule } from 'primeng/tag';
import { ConfirmDialogModule } from 'primeng/confirmdialog';
import { ConfirmationService, MessageService } from 'primeng/api';
import { FormsModule } from '@angular/forms';
import { InputIconModule } from 'primeng/inputicon';
import { IconFieldModule } from 'primeng/iconfield';

interface EDLEntry {
    id: string;
    value: string;
    description?: string;
    addedDate: Date;
    lastHit?: Date;
    hitCount: number;
}

interface Column {
    field: string;
    header: string;
}

@Component({
    selector: 'app-edl-details',
    standalone: true,
    imports: [
        CommonModule,
        TableModule,
        ButtonModule,
        RippleModule,
        ToastModule,
        ToolbarModule,
        InputTextModule,
        DialogModule,
        TagModule,
        ConfirmDialogModule,
        FormsModule,
        InputIconModule,
        IconFieldModule
    ],
    providers: [MessageService, ConfirmationService],
    templateUrl: './edl-details.html'
})
export class EdlDetails implements OnInit {
    entryDialog: boolean = false;
    entries = signal<EDLEntry[]>([]);
    entry!: EDLEntry;
    selectedEntries!: EDLEntry[] | null;
    submitted: boolean = false;
    edlType: 'IP' | 'URL' | 'DOMAIN' = 'IP'; // This would come from the parent component or route

    @ViewChild('dt') dt!: Table;

    cols!: Column[];

    constructor(
        private messageService: MessageService,
        private confirmationService: ConfirmationService
    ) {}

    ngOnInit() {
        // Simulated data - replace with actual service call
        this.entries.set([
            {
                id: '1',
                value: '192.168.1.1',
                description: 'Known malicious host',
                addedDate: new Date(),
                lastHit: new Date(),
                hitCount: 156
            }
        ]);

        this.cols = [
            { field: 'value', header: 'Value' },
            { field: 'description', header: 'Description' },
            { field: 'addedDate', header: 'Added Date' },
            { field: 'lastHit', header: 'Last Hit' },
            { field: 'hitCount', header: 'Hit Count' }
        ];
    }

    openNew() {
        this.entry = {
            id: '',
            value: '',
            description: '',
            addedDate: new Date(),
            hitCount: 0
        };
        this.submitted = false;
        this.entryDialog = true;
    }

    deleteSelectedEntries() {
        this.confirmationService.confirm({
            message: 'Are you sure you want to delete the selected entries?',
            header: 'Confirm',
            icon: 'pi pi-exclamation-triangle',
            accept: () => {
                this.entries.set(this.entries().filter(val => !this.selectedEntries?.includes(val)));
                this.selectedEntries = null;
                this.messageService.add({ severity: 'success', summary: 'Successful', detail: 'Entries Deleted', life: 3000 });
            }
        });
    }

    editEntry(entry: EDLEntry) {
        this.entry = { ...entry };
        this.entryDialog = true;
    }

    deleteEntry(entry: EDLEntry) {
        this.confirmationService.confirm({
            message: 'Are you sure you want to delete this entry?',
            header: 'Confirm',
            icon: 'pi pi-exclamation-triangle',
            accept: () => {
                this.entries.set(this.entries().filter(val => val.id !== entry.id));
                this.entry = {} as EDLEntry;
                this.messageService.add({ severity: 'success', summary: 'Successful', detail: 'Entry Deleted', life: 3000 });
            }
        });
    }

    hideDialog() {
        this.entryDialog = false;
        this.submitted = false;
    }

    saveEntry() {
        this.submitted = true;

        if (this.entry.value.trim()) {
            if (this.entry.id) {
                const entries = this.entries();
                const index = this.findIndexById(this.entry.id);
                entries[index] = this.entry;
                this.entries.set([...entries]);
                this.messageService.add({ severity: 'success', summary: 'Successful', detail: 'Entry Updated', life: 3000 });
            } else {
                this.entry.id = this.createId();
                this.entry.addedDate = new Date();
                this.entry.hitCount = 0;
                this.entries.set([...this.entries(), this.entry]);
                this.messageService.add({ severity: 'success', summary: 'Successful', detail: 'Entry Created', life: 3000 });
            }

            this.entryDialog = false;
            this.entry = {} as EDLEntry;
        }
    }

    findIndexById(id: string): number {
        return this.entries().findIndex(entry => entry.id === id);
    }

    createId(): string {
        let id = '';
        const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        for (let i = 0; i < 5; i++) {
            id += chars.charAt(Math.floor(Math.random() * chars.length));
        }
        return id;
    }

    onGlobalFilter(table: Table, event: Event) {
        table.filterGlobal((event.target as HTMLInputElement).value, 'contains');
    }

    validateEntry(value: string): boolean {
        // Add validation based on EDL type
        switch (this.edlType) {
            case 'IP':
                return this.validateIP(value);
            case 'URL':
                return this.validateURL(value);
            case 'DOMAIN':
                return this.validateDomain(value);
            default:
                return false;
        }
    }

    private validateIP(ip: string): boolean {
        const ipRegex = /^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
        return ipRegex.test(ip);
    }

    private validateURL(url: string): boolean {
        try {
            new URL(url);
            return true;
        } catch {
            return false;
        }
    }

    private validateDomain(domain: string): boolean {
        const domainRegex = /^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$/;
        return domainRegex.test(domain);
    }
}
