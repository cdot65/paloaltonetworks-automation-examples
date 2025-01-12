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
import { ActivatedRoute } from '@angular/router';
import { firstValueFrom } from 'rxjs';
import { EdlService } from '../../service/edl.service';
import { CreateEdlEntryDto, EDL, EDLEntry, EntryType, ListType } from '../../interfaces/edl.interface';
import { TooltipModule } from 'primeng/tooltip';

interface Column {
    field: string;
    header: string;
}

@Component({
    selector: 'app-edl-details',
    standalone: true,
    imports: [CommonModule, TableModule, ButtonModule, RippleModule, ToastModule, ToolbarModule, InputTextModule, DialogModule, TagModule, ConfirmDialogModule, FormsModule, InputIconModule, IconFieldModule, TooltipModule],
    providers: [MessageService, ConfirmationService],
    templateUrl: './edl-details.html'
})
export class EdlDetails implements OnInit {
    entryDialog: boolean = false;
    entries = signal<EDLEntry[]>([]);
    entry!: EDLEntry;
    selectedEntries!: EDLEntry[] | null;
    submitted: boolean = false;
    edlType: ListType = ListType.IP;
    edlId: string = '';
    edl: EDL | null = null;

    @ViewChild('dt') dt!: Table;

    cols!: Column[];

    constructor(
        private messageService: MessageService,
        private confirmationService: ConfirmationService,
        private route: ActivatedRoute,
        private edlService: EdlService
    ) {}

    ngOnInit() {
        this.route.params.subscribe((params) => {
            this.edlId = params['id']; // Updated to use id instead of name
            this.loadEdlDetails();
        });

        this.cols = [
            { field: 'address', header: 'Value' },
            { field: 'comment', header: 'Description' },
            { field: 'createdAt', header: 'Added Date' },
            { field: 'updatedAt', header: 'Last Updated' }
        ];
    }

    loadEdlDetails() {
        if (this.edlId) {
            this.edlService.getEdlList(this.edlId).subscribe({
                next: (edl) => {
                    this.edl = edl;
                    this.edlType = edl.type;
                    this.loadEntries();
                },
                error: (error) => {
                    this.messageService.add({
                        severity: 'error',
                        summary: 'Error',
                        detail: 'Failed to load EDL details',
                        life: 3000
                    });
                    console.error('Error loading EDL details:', error);
                }
            });
        }
    }

    loadEntries() {
        if (this.edlId) {
            this.edlService.getListEntries(this.edlId).subscribe({
                next: (entries) => {
                    this.entries.set(entries);
                },
                error: (error) => {
                    this.messageService.add({
                        severity: 'error',
                        summary: 'Error',
                        detail: 'Failed to load entries',
                        life: 3000
                    });
                    console.error('Error loading entries:', error);
                }
            });
        }
    }

    openNew() {
        this.entry = {
            id: '',
            address: '',
            comment: '',
            type: this.mapListTypeToEntryType(this.edlType),
            isEnabled: true,
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString(),
            listId: this.edlId
        } as EDLEntry;
        this.submitted = false;
        this.entryDialog = true;
    }

    // Add helper method to map between types
    private mapListTypeToEntryType(listType: ListType): EntryType {
        switch (listType) {
            case ListType.IP:
                return EntryType.IP;
            case ListType.URL:
                return EntryType.URL;
            case ListType.DOMAIN:
                return EntryType.DOMAIN;
            case ListType.EQUIPMENT_IDENTITY:
                return EntryType.IMEI;
            case ListType.SUBSCRIBER_IDENTITY:
                return EntryType.IMSI;
            default:
                return EntryType.IP;
        }
    }

    async deleteSelectedEntries() {
        this.confirmationService.confirm({
            message: 'Are you sure you want to delete the selected entries?',
            header: 'Confirm',
            icon: 'pi pi-exclamation-triangle',
            accept: async () => {
                if (this.selectedEntries) {
                    try {
                        const deletePromises = this.selectedEntries.map((entry) => firstValueFrom(this.edlService.deleteEntry(this.edlId, entry.id)));

                        await Promise.all(deletePromises);
                        this.loadEntries();
                        this.selectedEntries = null;
                        this.messageService.add({
                            severity: 'success',
                            summary: 'Successful',
                            detail: 'Selected entries deleted',
                            life: 3000
                        });
                    } catch (error) {
                        this.messageService.add({
                            severity: 'error',
                            summary: 'Error',
                            detail: 'Failed to delete selected entries',
                            life: 3000
                        });
                        console.error('Error deleting entries:', error);
                    }
                }
            }
        });
    }

    editEntry(entry: EDLEntry) {
        this.entry = { ...entry };
        this.entryDialog = true;
    }

    hideDialog() {
        this.entryDialog = false;
        this.submitted = false;
    }

    saveEntry() {
        this.submitted = true;

        if (this.entry.address?.trim() && this.validateEntry(this.entry.address)) {
            if (this.entry.id) {
                // Update existing entry
                const updateData = {
                    address: this.entry.address,
                    comment: this.entry.comment,
                    isEnabled: this.entry.isEnabled,
                    type: this.mapListTypeToEntryType(this.edlType)
                };

                this.edlService.updateEntry(this.edlId, this.entry.id, updateData).subscribe({
                    next: () => {
                        this.loadEntries();
                        this.messageService.add({
                            severity: 'success',
                            summary: 'Successful',
                            detail: 'Entry updated',
                            life: 3000
                        });
                        this.entryDialog = false;
                        this.entry = {} as EDLEntry;
                    },
                    error: (error) => {
                        this.messageService.add({
                            severity: 'error',
                            summary: 'Error',
                            detail: 'Failed to update entry',
                            life: 3000
                        });
                        console.error('Error updating entry:', error);
                    }
                });
            } else {
                // Create new entry
                const createDto: CreateEdlEntryDto = {
                    address: this.entry.address,
                    comment: this.entry.comment,
                    type: this.mapListTypeToEntryType(this.edlType),
                    isEnabled: true
                };

                this.edlService.createEntry(this.edlId, createDto).subscribe({
                    next: () => {
                        this.loadEntries();
                        this.messageService.add({
                            severity: 'success',
                            summary: 'Successful',
                            detail: 'Entry created',
                            life: 3000
                        });
                        this.entryDialog = false;
                        this.entry = {} as EDLEntry;
                    },
                    error: (error) => {
                        this.messageService.add({
                            severity: 'error',
                            summary: 'Error',
                            detail: 'Failed to create entry',
                            life: 3000
                        });
                        console.error('Error creating entry:', error);
                    }
                });
            }
        }
    }

    onGlobalFilter(table: Table, event: Event) {
        table.filterGlobal((event.target as HTMLInputElement).value, 'contains');
    }

    validateEntry(value: string): boolean {
        switch (this.edlType) {
            case ListType.IP:
                return this.validateIP(value);
            case ListType.URL:
                return this.validateURL(value);
            case ListType.DOMAIN:
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

    async exportPlaintext() {
        if (!this.edlId) return;

        this.edlService.getListPlaintext(this.edlId).subscribe({
            next: (plaintext) => {
                // Create blob and download
                const blob = new Blob([plaintext], { type: 'text/plain' });
                const url = window.URL.createObjectURL(blob);
                const link = document.createElement('a');
                link.href = url;
                // Use EDL name if available, otherwise use ID
                link.download = this.edl?.name ? `${this.edl.name}_entries.txt` : `edl_${this.edlId}_entries.txt`;
                link.click();
                window.URL.revokeObjectURL(url);
            },
            error: (error) => {
                this.messageService.add({
                    severity: 'error',
                    summary: 'Error',
                    detail: 'Failed to export plaintext',
                    life: 3000
                });
                console.error('Error exporting plaintext:', error);
            }
        });
    }
}
