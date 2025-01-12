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
import { EdlService } from '../service/edl.service';
import { EDL, EDLViewModel, CreateEdlListDto } from '../interfaces/edl.interface';

interface Column {
    field: string;
    header: string;
}

@Component({
    selector: 'app-edl-list',
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
        SelectModule,
        TagModule,
        TextareaModule,
        ConfirmDialogModule,
        FormsModule,
        InputIconModule,
        IconFieldModule
    ],
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
        { label: 'IP Address', value: 'IP' },
        { label: 'URL', value: 'URL' },
        { label: 'Domain', value: 'DOMAIN' }
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
            description: edl.description,
            type: edl.type,
            entryCount: edl.entries.length,
            lastUpdated: edl.updatedAt
        };
    }

    loadEdls() {
        this.edlService.getAllEdlLists().subscribe({
            next: (edls) => {
                const viewModels = edls.map(edl => this.transformToViewModel(edl));
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
            type: 'IP',
            entryCount: 0,
            lastUpdated: new Date().toISOString()
        };
        this.submitted = false;
        this.edlDialog = true;
    }

    deleteSelectedEdls() {
        this.confirmationService.confirm({
            message: 'Are you sure you want to delete the selected EDL lists?',
            header: 'Confirm',
            icon: 'pi pi-exclamation-triangle',
            accept: () => {
                // Note: Bulk delete not implemented in service yet
                this.messageService.add({
                    severity: 'info',
                    summary: 'Not Implemented',
                    detail: 'Bulk delete operation not available',
                    life: 3000
                });
            }
        });
    }

    editEdl(edl: EDLViewModel) {
        this.edl = { ...edl };
        this.edlDialog = true;
    }

    deleteEdl(edl: EDLViewModel) {
        this.confirmationService.confirm({
            message: 'Are you sure you want to delete ' + edl.name + '?',
            header: 'Confirm',
            icon: 'pi pi-exclamation-triangle',
            accept: () => {
                // Note: Delete not implemented in service yet
                this.messageService.add({
                    severity: 'info',
                    summary: 'Not Implemented',
                    detail: 'Delete operation not available',
                    life: 3000
                });
            }
        });
    }

    hideDialog() {
        this.edlDialog = false;
        this.submitted = false;
    }

    saveEdl() {
        this.submitted = true;

        if (this.edl.name.trim()) {
            const createEdlDto: CreateEdlListDto = {
                name: this.edl.name,
                description: this.edl.description,
                type: this.edl.type
            };

            this.edlService.createEdlList(createEdlDto).subscribe({
                next: () => {
                    this.loadEdls(); // Refresh the list
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

    async navigateToEdlDetails(edlName: string) {
        try {
            await this.router.navigate(['/edls', edlName]);
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
