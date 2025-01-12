import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
    standalone: true,
    selector: 'app-status-widget',
    imports: [CommonModule],
    templateUrl: './statuswidget.html',
    styleUrls: ['./statuswidget.scss']
})
export class StatusWidget {
    edlStatuses = [
        {
            name: 'IP Blocklist',
            count: '1,234',
            icon: 'ban',
            color: 'blue',
            status: '12 new',
            statusDetail: 'since last update'
        },
        {
            name: 'Domain Blocklist',
            count: '567',
            icon: 'globe',
            color: 'orange',
            status: '3 new',
            statusDetail: 'since last update'
        },
        {
            name: 'URL Blocklist',
            count: '890',
            icon: 'link',
            color: 'cyan',
            status: '5 new',
            statusDetail: 'since last update'
        },
        {
            name: 'Custom Lists',
            count: '123',
            icon: 'list',
            color: 'purple',
            status: '2 new',
            statusDetail: 'since last update'
        }
    ];
}
