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

    // EDL List CRUD Operations
    @Get()
    getAllLists() {
        return this.edlService.getAllLists();
    }

    @Post()
    createList(@Body() createEdlListDto: CreateEdlListDto) {
        return this.edlService.createList(createEdlListDto);
    }

    @Get(':id')
    getList(@Param('id', ParseUUIDPipe) id: string) {
        return this.edlService.getList(id);
    }

    @Patch(':id')
    updateList(
        @Param('id', ParseUUIDPipe) id: string,
        @Body() updateEdlListDto: UpdateEdlListDto,
    ) {
        return this.edlService.updateList(id, updateEdlListDto);
    }

    @Delete(':id')
    deleteList(@Param('id', ParseUUIDPipe) id: string) {
        return this.edlService.deleteList(id);
    }

    // EDL Entries Operations
    @Get(':id/entries')
    getListEntries(@Param('id', ParseUUIDPipe) id: string) {
        return this.edlService.getListEntries(id);
    }

    @Post(':id/entries')
    async createEntry(
        @Param('id', ParseUUIDPipe) listId: string,
        @Body() createEdlEntryDto: CreateEdlEntryDto,
    ) {
        // Create a new object with the listId from the URL parameter
        const entryData = {
            ...createEdlEntryDto,
            listId, // Add the listId from the URL parameter
        };

        return this.edlService.createEntry(entryData);
    }

    @Patch(':listId/entries/:entryId')
    updateEntry(
        @Param('listId', ParseUUIDPipe) listId: string,
        @Param('entryId', ParseUUIDPipe) entryId: string,
        @Body() updateEdlEntryDto: UpdateEdlEntryDto,
    ) {
        // Ensure the listId matches the URL parameter
        updateEdlEntryDto.listId = listId;
        return this.edlService.updateEntry(entryId, updateEdlEntryDto);
    }

    @Delete(':listId/entries/:entryId')
    deleteEntry(
        @Param('listId', ParseUUIDPipe) listId: string,
        @Param('entryId', ParseUUIDPipe) entryId: string,
    ) {
        return this.edlService.deleteEntry(entryId);
    }

    // Plaintext Export
    @Get(':id/plaintext')
    @Header('Content-Type', 'text/plain')
    getListPlaintext(@Param('id', ParseUUIDPipe) id: string) {
        return this.edlService.getListPlaintext(id);
    }
}
