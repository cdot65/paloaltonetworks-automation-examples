// backend/src/app.service.ts
import { Injectable } from '@nestjs/common';

@Injectable()
export class AppService {
    getHealth(): { status: string; timestamp: string } {
        return {
            status: 'healthy',
            timestamp: new Date().toISOString(),
        };
    }
}
