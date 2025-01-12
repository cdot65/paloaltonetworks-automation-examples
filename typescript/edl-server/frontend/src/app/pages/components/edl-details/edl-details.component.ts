// src/app/pages/components/edl-details/edl-details.component.ts
import { Component, OnDestroy, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import {
    EDL,
    EdlEntry,
    EdlType
} from '../../interfaces/edl.interface';
import { EdlService } from '../../services/edl.service';
import { firstValueFrom, Subject, takeUntil } from 'rxjs';
import { ModalComponent } from '../../../shared/components/modal/modal.component';
import {
    ModalField,
    ModalFormData,
} from '../../../shared/interfaces/modal.interface';

@Component({
    selector: 'app-edl-details',
    standalone: true,
    imports: [CommonModule, FormsModule, ModalComponent, ReactiveFormsModule],
    templateUrl: './edl-details.component.html',
    styleUrl: './edl-details.component.css',
})
export class EdlDetailsComponent implements OnInit, OnDestroy {
    edl: EDL | null = null;
    entries: EdlEntry[] = [];
    isLoading = false;
    error: string | null = null;
    searchTerm = '';

    // Modal properties
    isModalOpen = false;
    modalFields: ModalField[] = [
        {
            name: 'address',
            label: 'Address',
            type: 'text',
            placeholder: 'Enter IP address, URL, or domain',
            required: true,
        },
        {
            name: 'comment',
            label: 'Comment',
            type: 'textarea',
            placeholder: 'Enter a description or comment',
        },
    ];

    private destroy$ = new Subject<void>();
    private listName: string | null = null;

    constructor(
        private route: ActivatedRoute,
        private edlService: EdlService,
    ) {}

    ngOnInit(): void {
        console.log('EdlDetailsComponent init');
        this.route.params.pipe(takeUntil(this.destroy$)).subscribe((params) => {
            this.listName = params['name'];
            if (this.listName) {
                this.loadEdlDetails(this.listName);
            }
        });
    }

    ngOnDestroy(): void {
        this.destroy$.next();
        this.destroy$.complete();
    }

    private loadEdlDetails(name: string): void {
        this.isLoading = true;
        this.error = null;

        this.edlService
            .getEdlListByName(name)
            .pipe(takeUntil(this.destroy$))
            .subscribe({
                next: (edl) => {
                    this.edl = edl;
                    this.entries = edl.entries || []; // Set entries from EDL response
                    this.isLoading = false;
                },
                error: (err) => {
                    console.error('Error loading EDL details:', err);
                    this.error =
                        'Failed to load EDL details. Please try again.';
                    this.isLoading = false;
                },
            });
    }

    get filteredEntries(): EdlEntry[] {
        return this.entries.filter(
            (entry) =>
                entry.address
                    .toLowerCase()
                    .includes(this.searchTerm.toLowerCase()) ||
                entry.comment
                    ?.toLowerCase()
                    .includes(this.searchTerm.toLowerCase()),
        );
    }

    async createEntry(entry: Partial<EdlEntry> & { type?: EdlType }): Promise<void> {
        if (!this.listName || !this.edl?.type) return;

        try {
            const newEntry = await firstValueFrom(
                this.edlService.createEdlEntry({
                    address: entry.address!,
                    comment: entry.comment,
                    type: this.edl.type as EdlType, // Explicitly type cast
                    listName: this.listName,
                }),
            );

            if (newEntry) {
                this.entries = [...this.entries, newEntry];
            }
        } catch (err) {
            console.error('Error creating entry:', err);
            this.error = 'Failed to create entry. Please try again.';
        }
    }

    async toggleEntryStatus(entry: EdlEntry): Promise<void> {
        try {
            const updatedEntry = await firstValueFrom(
                this.edlService.updateEntry(entry.id, {
                    ...entry,
                    isEnabled: !entry.isEnabled,
                }),
            );

            if (updatedEntry) {
                this.entries = this.entries.map((e) =>
                    e.id === updatedEntry.id ? updatedEntry : e,
                );
            }
        } catch (err) {
            console.error('Error updating entry:', err);
            this.error = 'Failed to update entry. Please try again.';
        }
    }

    async deleteEntry(entryId: string): Promise<void> {
        try {
            await firstValueFrom(this.edlService.deleteEntry(entryId));
            this.entries = this.entries.filter((e) => e.id !== entryId);
        } catch (err) {
            console.error('Error deleting entry:', err);
            this.error = 'Failed to delete entry. Please try again.';
        }
    }

    // Open modal for new EDL entry
    openCreateEntryDialog(): void {
        console.log('Opening modal...');
        this.isModalOpen = true;
        console.log('Modal open state:', this.isModalOpen);
    }

    // handle submission.
    async handleModalSubmit(formData: ModalFormData): Promise<void> {
        console.log('Form submitted:', formData);
        await this.createEntry({
            address: formData['address'],
            comment: formData['comment'],
            type: this.edl?.type as EdlType
        });
    }

    clearSearch(): void {
        this.searchTerm = '';
    }
}
