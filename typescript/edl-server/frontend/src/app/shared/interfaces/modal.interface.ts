// src/app/shared/interfaces/modal.interface.ts
import { AbstractControl } from '@angular/forms';

export interface ModalField {
    name: string;
    label: string;
    type: 'text' | 'textarea' | 'select' | 'number';
    placeholder?: string;
    options?: { value: string; label: string }[];
    required?: boolean;
}

export type ModalFormData = Record<string, string>;

export type FormGroupControls = Record<string, AbstractControl>;
