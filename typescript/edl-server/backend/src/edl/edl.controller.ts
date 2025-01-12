// backend/src/edl/edl.controller.ts
import {
    Controller,
    Get,
    Post,
    Body,
    Patch,
    Param,
    Delete,
    Header,
    ParseUUIDPipe,
} from '@nestjs/common';
import { EdlService } from './edl.service';
import { CreateEdlListDto } from './dto/create-edl-list.dto';
import { CreateEdlEntryDto } from './dto/create-edl-entry.dto';
import { UpdateEdlListDto } from './dto/update-edl-list.dto';
import { UpdateEdlEntryDto } from './dto/update-edl-entry.dto';

@Controller('edl')
export class EdlController {
    constructor(private readonly edlService: EdlService) {}

    // List Management Endpoints
    @Post('lists')
    createList(@Body() createEdlListDto: CreateEdlListDto) {
        return this.edlService.createList(createEdlListDto);
    }

    @Get('lists')
    getAllLists() {
        return this.edlService.getAllLists();
    }

    @Get('lists/:name')
    getList(@Param('name') name: string) {
        return this.edlService.getList(name);
    }

    @Patch('lists/:name')
    updateList(
        @Param('name') name: string,
        @Body() updateEdlListDto: UpdateEdlListDto,
    ) {
        return this.edlService.updateList(name, updateEdlListDto);
    }

    @Delete('lists/:name')
    deleteList(@Param('name') name: string) {
        return this.edlService.deleteList(name);
    }

    // Entry Management Endpoints
    @Post('entries')
    createEntry(@Body() createEdlEntryDto: CreateEdlEntryDto) {
        return this.edlService.createEntry(createEdlEntryDto);
    }

    @Get('entries/:id')
    getEntry(@Param('id', ParseUUIDPipe) id: string) {
        return this.edlService.getEntry(id);
    }

    @Patch('entries/:id')
    updateEntry(
        @Param('id', ParseUUIDPipe) id: string,
        @Body() updateEdlEntryDto: UpdateEdlEntryDto,
    ) {
        return this.edlService.updateEntry(id, updateEdlEntryDto);
    }

    @Delete('entries/:id')
    deleteEntry(@Param('id', ParseUUIDPipe) id: string) {
        return this.edlService.deleteEntry(id);
    }

    // Plaintext Export Endpoint
    @Get(':name/plaintext')
    @Header('Content-Type', 'text/plain')
    getListPlaintext(@Param('name') name: string) {
        return this.edlService.getListPlaintext(name);
    }
}
