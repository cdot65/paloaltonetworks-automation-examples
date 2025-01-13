// src/app/layout/component/app.topbar.ts
import { Component } from '@angular/core';
import { MenuItem } from 'primeng/api';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { StyleClassModule } from 'primeng/styleclass';
import { AppConfigurator } from './app.configurator';
import { LayoutService } from '../service/layout.service';

@Component({
    selector: 'app-topbar',
    standalone: true,
    imports: [RouterModule, CommonModule, StyleClassModule, AppConfigurator],
    template: ` <div class="layout-topbar">
        <div class="layout-topbar-logo-container">
            <button class="layout-menu-button layout-topbar-action" (click)="layoutService.onMenuToggle()">
                <i class="pi pi-bars"></i>
            </button>
            <a class="layout-topbar-logo" routerLink="/">
                <svg id="Layer_1" data-name="Layer 1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1268.76 1400">
                    <defs>
                        <style>
                            .cls-1 {
                                fill: var(--primary-color);
                            }
                        </style>
                    </defs>
                    <path
                        class="cls-1"
                        d="M1175.73,495.78c-80.1-105.47-196.97-186.01-333.76-226.59-18.26-15.71-28.84-42.03-28.61-84.54.37-85.15,40.27-131.85,72.58-184.23-36.53-5.95-129.65,51.8-169.99,132.51-7.89-50.97-40.79-113.81-72.15-132.51-24.06,10.53-66.33,83.37-68.85,133.19C559.78,100.27,492.17,8.24,393.75.42c35.63,38.08,82.5,103.63,83.14,169.95.53,57.12-10.28,78.68-29.59,95.97-152.55,42.84-281.13,135.27-362.87,256.57C23.99,612.6,0,718.07,0,830.97c0,133.71,38.03,256.98,120.43,356.03,118.78,142.7,307.2,213,519.37,213,181.73,0,346.04-45.78,464.09-154.87,115.39-106.64,164.86-252.88,164.86-414.16,0-124.47-20.68-239.94-93.02-335.19Z"
                    />
                </svg>
                <span>Pomegranate</span>
            </a>
        </div>

        <div class="layout-topbar-actions">
            <div class="layout-config-menu">
                <button type="button" class="layout-topbar-action" (click)="toggleDarkMode()">
                    <i [ngClass]="{ 'pi ': true, 'pi-moon': layoutService.isDarkTheme(), 'pi-sun': !layoutService.isDarkTheme() }"></i>
                </button>
                <div class="relative">
                    <button
                        class="layout-topbar-action layout-topbar-action-highlight"
                        pStyleClass="@next"
                        enterFromClass="hidden"
                        enterActiveClass="animate-scalein"
                        leaveToClass="hidden"
                        leaveActiveClass="animate-fadeout"
                        [hideOnOutsideClick]="true"
                    >
                        <i class="pi pi-palette"></i>
                    </button>
                    <app-configurator />
                </div>
            </div>

            <button class="layout-topbar-menu-button layout-topbar-action" pStyleClass="@next" enterFromClass="hidden" enterActiveClass="animate-scalein" leaveToClass="hidden" leaveActiveClass="animate-fadeout" [hideOnOutsideClick]="true">
                <i class="pi pi-ellipsis-v"></i>
            </button>

            <div class="layout-topbar-menu hidden lg:block">
                <div class="layout-topbar-menu-content">
                    <button type="button" class="layout-topbar-action">
                        <i class="pi pi-user"></i>
                        <span>Profile</span>
                    </button>
                </div>
            </div>
        </div>
    </div>`
})
export class AppTopbar {
    items!: MenuItem[];

    constructor(public layoutService: LayoutService) {}

    toggleDarkMode() {
        this.layoutService.layoutConfig.update((state) => ({ ...state, darkTheme: !state.darkTheme }));
    }
}
