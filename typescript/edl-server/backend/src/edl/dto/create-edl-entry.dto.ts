// backend/src/edl/dto/create-edl-entry.dto.ts
import { IsString, IsOptional, IsEnum, IsBoolean } from 'class-validator';
import { EntryType } from '../types/edl.types';

export class CreateEdlEntryDto {
    @IsString()
    address: string;

    @IsOptional()
    @IsString()
    comment?: string;

    @IsEnum(EntryType)
    type: EntryType;

    @IsBoolean()
    @IsOptional()
    isEnabled?: boolean;

    @IsOptional()
    @IsString()
    createdBy?: string;
}
