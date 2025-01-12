// src/app/shared/components/modal/modal.component.ts
import { Component, EventEmitter, Input, Output, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule, FormGroup, FormBuilder, Validators } from '@angular/forms';
import { ModalField, ModalFormData, FormGroupControls } from '../../interfaces/modal.interface';

@Component({
    selector: 'app-modal',
    standalone: true,
    imports: [CommonModule, FormsModule, ReactiveFormsModule],
    templateUrl: './modal.component.html'
})
export class ModalComponent implements OnInit {
    @Input() title = '';
    @Input() isOpen = false;
    @Input() fields: ModalField[] = [];
    @Output() closeModal = new EventEmitter<void>();
    @Output() submitForm = new EventEmitter<ModalFormData>();

    form: FormGroup;

    constructor(private fb: FormBuilder) {
        this.form = this.fb.group({});
    }

    ngOnInit() {
        console.log(this.fields);
        const group: FormGroupControls = {};
        this.fields.forEach(field => {
            group[field.name] = this.fb.control('', field.required ? Validators.required : []);
        });
        this.form = this.fb.group(group);
    }

    onSubmit() {
        if (this.form.valid) {
            this.submitForm.emit(this.form.value);
            this.form.reset();
            this.closeModal.emit();
        }
    }

    onClose() {
        this.form.reset();
        this.closeModal.emit();
    }
}
