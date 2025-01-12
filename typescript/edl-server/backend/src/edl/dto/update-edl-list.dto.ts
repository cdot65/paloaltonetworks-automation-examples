// backend/src/edl/dto/update-edl-list.dto.ts
import { PartialType } from '@nestjs/mapped-types';
import { CreateEdlListDto } from './create-edl-list.dto';

export class UpdateEdlListDto extends PartialType(CreateEdlListDto) {}
