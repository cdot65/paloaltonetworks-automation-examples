// backend/src/edl/dto/update-edl-entry.dto.ts
import { PartialType } from '@nestjs/mapped-types';
import { CreateEdlEntryDto } from './create-edl-entry.dto';

export class UpdateEdlEntryDto extends PartialType(CreateEdlEntryDto) {}
