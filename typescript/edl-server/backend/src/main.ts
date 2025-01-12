// backend/src/main.ts
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { ConfigService } from '@nestjs/config';
import { Logger, ValidationPipe } from '@nestjs/common';

const logger = new Logger('Bootstrap');

async function bootstrap(): Promise<void> {
    try {
        // Set logger level to include debug messages
        logger.debug('Starting application...');

        const app = await NestFactory.create(AppModule, {
            logger: ['error', 'warn', 'log', 'debug', 'verbose'], // Include debug level
        });

        // Get the ConfigService instance
        const configService = app.get(ConfigService);

        // Get the frontend URL from the environment variables
        const frontendUrl = configService.get<string>('FRONTEND_URL');

        // Add global prefix here
        app.setGlobalPrefix('api/v1');

        // validation pipe enabled globally
        app.useGlobalPipes(new ValidationPipe({ transform: true }));

        // Enable CORS
        app.enableCors({
            origin: ['*', 'https://localhost', 'http://localhost', frontendUrl],
            methods: 'GET,HEAD,PUT,PATCH,POST,DELETE',
            credentials: true,
        });

        await app.listen(3000);
        logger.log('Application is running on port 3000');
    } catch (error) {
        logger.error('Failed to start application:', error);
        process.exit(1);
    }
}

void bootstrap();
