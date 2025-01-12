import { Component, OnInit, signal, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { Table, TableModule } from 'primeng/table';
import { ButtonModule } from 'primeng/button';
import { RippleModule } from 'primeng/ripple';
import { ToastModule } from 'primeng/toast';
import { ToolbarModule } from 'primeng/toolbar';
import { InputTextModule } from 'primeng/inputtext';
import { DialogModule } from 'primeng/dialog';
import { SelectModule } from 'primeng/select';
import { TagModule } from 'primeng/tag';
import { TextareaModule } from 'primeng/textarea';
import { ConfirmDialogModule } from 'primeng/confirmdialog';
import { ConfirmationService, MessageService } from 'primeng/api';
import { FormsModule } from '@angular/forms';
import { InputIconModule } from 'primeng/inputicon';
import { IconFieldModule } from 'primeng/iconfield';
import { firstValueFrom } from 'rxjs';
import { EdlService } from '../../service/edl.service';
import { EDL, EDLViewModel, CreateEdlListDto, ListType } from '../../interfaces/edl.interface';

interface Column {
    field: string;
    header: string;
}

@Component({
    selector: 'app-edl-list',
    standalone: true,
    imports: [CommonModule, TableModule, ButtonModule, RippleModule, ToastModule, ToolbarModule, InputTextModule, DialogModule, SelectModule, TagModule, TextareaModule, ConfirmDialogModule, FormsModule, InputIconModule, IconFieldModule],
    providers: [MessageService, ConfirmationService],
    templateUrl: './edl-list.html'
})
export class EdlList implements OnInit {
    edlDialog: boolean = false;
    edls = signal<EDLViewModel[]>([]);
    edl!: EDLViewModel;
    selectedEdls!: EDLViewModel[] | null;
    submitted: boolean = false;

    @ViewChild('dt') dt!: Table;

    cols!: Column[];

    edlTypes = [
        { label: 'IP Address', value: ListType.IP },
        { label: 'URL', value: ListType.URL },
        { label: 'Domain', value: ListType.DOMAIN }
    ];

    constructor(
        private messageService: MessageService,
        private confirmationService: ConfirmationService,
        private edlService: EdlService,
        private router: Router
    ) {}

    ngOnInit() {
        this.loadEdls();

        this.cols = [
            { field: 'name', header: 'Name' },
            { field: 'type', header: 'Type' },
            { field: 'entryCount', header: 'Entries' },
            { field: 'lastUpdated', header: 'Last Updated' }
        ];
    }

    transformToViewModel(edl: EDL): EDLViewModel {
        return {
            id: edl.id,
            name: edl.name,
            description: edl.description ?? '',
            type: edl.type,
            entryCount: edl.entries?.length ?? 0,
            lastUpdated: edl.updatedAt
        };
    }

    loadEdls() {
        this.edlService.getAllEdlLists().subscribe({
            next: (edls) => {
                const viewModels = edls.map((edl) => this.transformToViewModel(edl));
                this.edls.set(viewModels);
            },
            error: (error) => {
                this.messageService.add({
                    severity: 'error',
                    summary: 'Error',
                    detail: 'Failed to load EDLs',
                    life: 3000
                });
                console.error('Error loading EDLs:', error);
            }
        });
    }

    openNew() {
        this.edl = {
            id: '',
            name: '',
            description: '',
            type: ListType.IP,
            entryCount: 0,
            lastUpdated: new Date().toISOString()
        };
        this.submitted = false;
        this.edlDialog = true;
    }

    editEdl(edl: EDLViewModel) {
        this.edl = { ...edl };
        this.edlDialog = true;
    }

    hideDialog() {
        this.edlDialog = false;
        this.submitted = false;
    }

    saveEdl() {
        this.submitted = true;

        if (this.edl.name.trim()) {
            const edlDto: CreateEdlListDto = {
                name: this.edl.name,
                description: this.edl.description,
                type: this.edl.type
            };

            // If we have an ID, it's an update operation
            if (this.edl.id) {
                this.edlService.updateEdlList(this.edl.id, edlDto).subscribe({
                    next: () => {
                        this.loadEdls();
                        this.messageService.add({
                            severity: 'success',
                            summary: 'Successful',
                            detail: 'EDL Updated',
                            life: 3000
                        });
                        this.edlDialog = false;
                        this.edl = {} as EDLViewModel;
                    },
                    error: (error) => {
                        this.messageService.add({
                            severity: 'error',
                            summary: 'Error',
                            detail: 'Failed to update EDL',
                            life: 3000
                        });
                        console.error('Error updating EDL:', error);
                    }
                });
            } else {
                this.edlService.createEdlList(edlDto).subscribe({
                    next: () => {
                        this.loadEdls();
                        this.messageService.add({
                            severity: 'success',
                            summary: 'Successful',
                            detail: 'EDL Created',
                            life: 3000
                        });
                        this.edlDialog = false;
                        this.edl = {} as EDLViewModel;
                    },
                    error: (error) => {
                        this.messageService.add({
                            severity: 'error',
                            summary: 'Error',
                            detail: 'Failed to create EDL',
                            life: 3000
                        });
                        console.error('Error creating EDL:', error);
                    }
                });
            }
        }
    }

    async deleteSelectedEdls() {
        this.confirmationService.confirm({
            message: 'Are you sure you want to delete the selected EDL lists?',
            header: 'Confirm',
            icon: 'pi pi-exclamation-triangle',
            accept: async () => {
                if (this.selectedEdls) {
                    try {
                        const deletePromises = this.selectedEdls.map((edl) => firstValueFrom(this.edlService.deleteEdlList(edl.id)));

                        await Promise.all(deletePromises);
                        this.loadEdls();
                        this.selectedEdls = null;
                        this.messageService.add({
                            severity: 'success',
                            summary: 'Successful',
                            detail: 'Selected EDLs Deleted',
                            life: 3000
                        });
                    } catch (error) {
                        this.messageService.add({
                            severity: 'error',
                            summary: 'Error',
                            detail: 'Failed to delete selected EDLs',
                            life: 3000
                        });
                        console.error('Error deleting selected EDLs:', error);
                    }
                }
            }
        });
    }

    onGlobalFilter(table: Table, event: Event) {
        table.filterGlobal((event.target as HTMLInputElement).value, 'contains');
    }

    getSeverity(type: string): 'success' | 'info' | 'warn' {
        switch (type) {
            case 'IP':
                return 'info';
            case 'URL':
                return 'warn';
            case 'DOMAIN':
                return 'success';
            default:
                return 'info';
        }
    }

    async navigateToEdlDetails(edlId: string) {
        try {
            await this.router.navigate(['edl', edlId]);
        } catch (error) {
            console.error('Navigation error:', error);
            this.messageService.add({
                severity: 'error',
                summary: 'Error',
                detail: 'Failed to navigate to EDL details',
                life: 3000
            });
        }
    }
}
