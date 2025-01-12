// backend/src/edl/dto/create-edl-list.dto.ts
import { IsString, IsOptional, IsEnum } from 'class-validator';
import { ListType } from '../types/edl.types';

export class CreateEdlListDto {
    @IsString()
    name: string;

    @IsOptional()
    @IsString()
    description?: string;

    @IsEnum(ListType)
    type: ListType;

    @IsOptional()
    @IsString()
    createdBy?: string;
}
