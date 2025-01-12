// backend/src/edl/edl.module.ts
import { Module } from '@nestjs/common';
import { EdlService } from './edl.service';
import { EdlController } from './edl.controller';
import { PrismaModule } from '../prisma/prisma.module';

@Module({
    imports: [PrismaModule],
    controllers: [EdlController],
    providers: [EdlService],
    exports: [EdlService],
})
export class EdlModule {}
