// backend/src/edl/edl.service.ts
import { Injectable, Logger, NotFoundException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { CreateEdlListDto } from './dto/create-edl-list.dto';
import { CreateEdlEntryDto } from './dto/create-edl-entry.dto';
import { UpdateEdlListDto } from './dto/update-edl-list.dto';
import { UpdateEdlEntryDto } from './dto/update-edl-entry.dto';
import { EntryType, ListType } from './types/edl.types';
import { EdlEntry, EdlList } from './interfaces/edl.interface';

@Injectable()
export class EdlService {
    private readonly logger = new Logger(EdlService.name);

    constructor(private prisma: PrismaService) {}

    private mapToEdlList = (list: any): EdlList => ({
        ...list,
        type: list.type as ListType,
        entries: list.entries?.map(this.mapToEdlEntry),
    });

    private mapToEdlEntry = (entry: any): EdlEntry => ({
        ...entry,
        type: entry.type as EntryType,
        list: entry.list ? this.mapToEdlList(entry.list) : undefined,
    });

    async createList(createEdlListDto: CreateEdlListDto): Promise<EdlList> {
        const list = await this.prisma.edlList.create({
            data: createEdlListDto,
        });
        return this.mapToEdlList(list);
    }

    async getAllLists(): Promise<EdlList[]> {
        const lists = await this.prisma.edlList.findMany({
            include: { entries: true },
        });
        return lists.map((list) => this.mapToEdlList(list));
    }

    async getList(name: string): Promise<EdlList> {
        const list = await this.prisma.edlList.findUnique({
            where: { name },
            include: { entries: true },
        });
        if (!list) throw new NotFoundException(`EDL List ${name} not found`);
        return this.mapToEdlList(list);
    }

    async updateList(
        name: string,
        updateEdlListDto: UpdateEdlListDto,
    ): Promise<EdlList> {
        await this.getList(name);
        const list = await this.prisma.edlList.update({
            where: { name },
            data: updateEdlListDto,
        });
        return this.mapToEdlList(list);
    }

    async deleteList(name: string): Promise<EdlList> {
        await this.getList(name);
        const list = await this.prisma.edlList.delete({
            where: { name },
        });
        return this.mapToEdlList(list);
    }

    async createEntry(createEdlEntryDto: CreateEdlEntryDto): Promise<EdlEntry> {
        await this.getList(createEdlEntryDto.listName);
        const entry = await this.prisma.edlEntry.create({
            data: createEdlEntryDto,
        });
        return this.mapToEdlEntry(entry);
    }

    async getEntry(id: string): Promise<EdlEntry> {
        const entry = await this.prisma.edlEntry.findUnique({
            where: { id },
            include: { list: true },
        });
        if (!entry)
            throw new NotFoundException(`EDL Entry with ID ${id} not found`);
        return this.mapToEdlEntry(entry);
    }

    async updateEntry(
        id: string,
        updateEdlEntryDto: UpdateEdlEntryDto,
    ): Promise<EdlEntry> {
        await this.getEntry(id);
        if (updateEdlEntryDto.listName) {
            await this.getList(updateEdlEntryDto.listName);
        }
        const entry = await this.prisma.edlEntry.update({
            where: { id },
            data: updateEdlEntryDto,
        });
        return this.mapToEdlEntry(entry);
    }

    async deleteEntry(id: string): Promise<EdlEntry> {
        await this.getEntry(id);
        const entry = await this.prisma.edlEntry.delete({
            where: { id },
        });
        return this.mapToEdlEntry(entry);
    }

    async getListPlaintext(name: string): Promise<string> {
        this.logger.debug(`Generating plaintext for EDL list: ${name}`);
        const list = await this.getList(name);

        // Only include enabled entries and format based on list type
        return list.entries
            .filter((entry: EdlEntry) => entry.isEnabled)
            .map((entry: EdlEntry) => {
                switch (list.type) {
                    case ListType.IP:
                        return `${entry.address}`;
                    case ListType.DOMAIN:
                    case ListType.URL:
                        // Strip protocol if present and ensure trailing slash for URLs
                        const cleanAddress = entry.address.replace(
                            /^(http|https):\/\//,
                            '',
                        );
                        return list.type === ListType.URL &&
                            !cleanAddress.endsWith('/')
                            ? `${cleanAddress}/`
                            : cleanAddress;
                    default:
                        return entry.address;
                }
            })
            .sort()
            .join('\n');
    }
}
