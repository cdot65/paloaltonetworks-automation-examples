// backend/src/app.module.ts
import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { PrismaModule } from './prisma/prisma.module';
import { EdlModule } from './edl/edl.module';
import * as Joi from '@hapi/joi';

@Module({
    imports: [
        ConfigModule.forRoot({
            isGlobal: true,
            validationSchema: Joi.object({
                DATABASE_URL: Joi.string().required(),
                FRONTEND_URL: Joi.string().required(),
                // Add other env validations as needed
            }),
        }),
        PrismaModule,
        EdlModule,
    ],
    controllers: [AppController],
    providers: [AppService],
})
export class AppModule {}
