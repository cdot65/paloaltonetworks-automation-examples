// backend/src/edl/dto/update-edl-entry.dto.ts
import { PartialType } from '@nestjs/mapped-types';
import { CreateEdlEntryDto } from './create-edl-entry.dto';
import { IsOptional, IsUUID } from 'class-validator';

export class UpdateEdlEntryDto extends PartialType(CreateEdlEntryDto) {
    @IsOptional()
    @IsUUID()
    listId?: string;
}
