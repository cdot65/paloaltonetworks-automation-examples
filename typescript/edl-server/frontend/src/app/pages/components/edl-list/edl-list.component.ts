// src/app/pages/components/edl-list/edl-list.component.ts
import { Component, OnDestroy, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { EDL, EdlType } from '../../interfaces/edl.interface';
import { EdlService } from '../../services/edl.service';
import { firstValueFrom, Subject, takeUntil } from 'rxjs';
import { ModalComponent } from '../../../shared/components/modal/modal.component';
import {
    ModalField,
    ModalFormData,
} from '../../../shared/interfaces/modal.interface';

@Component({
    selector: 'app-edl-list',
    standalone: true,
    imports: [
        CommonModule,
        RouterLink,
        FormsModule,
        ReactiveFormsModule,
        ModalComponent,
    ],
    templateUrl: './edl-list.component.html',
    styleUrl: './edl-list.component.css',
})
export class EdlListComponent implements OnInit, OnDestroy {
    edls: EDL[] = [];
    isLoading = false;
    error: string | null = null;
    private destroy$ = new Subject<void>();

    // Modal properties
    isModalOpen = false;
    modalFields: ModalField[] = [
        {
            name: 'name',
            label: 'List Name',
            type: 'text',
            placeholder: 'Enter a unique name for the EDL list',
            required: true,
        },
        {
            name: 'description',
            label: 'Description',
            type: 'textarea',
            placeholder: 'Enter a description for the EDL list',
        },
        {
            name: 'type',
            label: 'Type',
            type: 'select',
            required: true,
            options: [
                { value: 'IP', label: 'IP Address' },
                { value: 'URL', label: 'URL' },
                { value: 'DOMAIN', label: 'Domain' },
                { value: 'IMEI', label: 'IMEI' },
                { value: 'IMSI', label: 'IMSI' },
            ],
        },
    ];

    constructor(private edlService: EdlService) {}

    ngOnInit(): void {
        this.loadEdlLists();
    }

    ngOnDestroy(): void {
        this.destroy$.next();
        this.destroy$.complete();
    }

    loadEdlLists(): void {
        this.isLoading = true;
        this.error = null;

        this.edlService
            .getAllEdlLists()
            .pipe(takeUntil(this.destroy$))
            .subscribe({
                next: (lists) => {
                    this.edls = lists;
                    this.isLoading = false;
                },
                error: (err) => {
                    console.error('Error loading EDL lists:', err);
                    this.error = 'Failed to load EDL lists. Please try again.';
                    this.isLoading = false;
                },
            });
    }

    getTypeClass(type: string): string {
        switch (type) {
            case 'IP':
                return 'bg-blue-500/20 text-blue-400';
            case 'URL':
                return 'bg-purple-500/20 text-purple-400';
            case 'DOMAIN':
                return 'bg-green-500/20 text-green-400';
            default:
                return 'bg-gray-500/20 text-gray-400';
        }
    }

    getEntryCount(edl: EDL): number {
        return edl.entries?.length ?? 0;
    }

    // Modal handlers
    openCreateEdlDialog(): void {
        this.isModalOpen = true;
    }

    async handleModalSubmit(formData: ModalFormData): Promise<void> {
        try {
            const newEdl = await firstValueFrom(
                this.edlService.createEdlList({
                    name: formData['name'],
                    description: formData['description'] || '',
                    type: formData['type'] as EdlType,
                }),
            );

            if (newEdl) {
                this.edls = [...this.edls, newEdl];
                this.error = null;
            }
        } catch (err) {
            console.error('Error creating EDL list:', err);
            this.error = 'Failed to create EDL list. Please try again.';
        }
    }
}
