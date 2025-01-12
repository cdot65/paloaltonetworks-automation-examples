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
            include: { entries: true },
        });
        return this.mapToEdlList(list);
    }

    async getAllLists(): Promise<EdlList[]> {
        const lists = await this.prisma.edlList.findMany({
            include: { entries: true },
        });
        return lists.map((list) => this.mapToEdlList(list));
    }

    async getList(id: string): Promise<EdlList> {
        const list = await this.prisma.edlList.findUnique({
            where: { id },
            include: { entries: true },
        });
        if (!list) throw new NotFoundException(`EDL List ${id} not found`);
        return this.mapToEdlList(list);
    }

    async updateList(
        id: string,
        updateEdlListDto: UpdateEdlListDto,
    ): Promise<EdlList> {
        const existingList = await this.getList(id);

        // If name is being updated, check if new name is available
        if (
            updateEdlListDto.name &&
            updateEdlListDto.name !== existingList.name
        ) {
            const nameExists = await this.prisma.edlList.findUnique({
                where: { name: updateEdlListDto.name },
            });
            if (nameExists) {
                throw new Error(
                    `EDL List with name ${updateEdlListDto.name} already exists`,
                );
            }
        }

        const list = await this.prisma.edlList.update({
            where: { id },
            data: updateEdlListDto,
            include: { entries: true },
        });
        return this.mapToEdlList(list);
    }

    async deleteList(id: string): Promise<EdlList> {
        await this.getList(id);
        const list = await this.prisma.edlList.delete({
            where: { id },
            include: { entries: true },
        });
        return this.mapToEdlList(list);
    }

    async getListByName(name: string): Promise<EdlList | null> {
        const list = await this.prisma.edlList.findUnique({
            where: { name },
            include: { entries: true },
        });
        return list ? this.mapToEdlList(list) : null;
    }

    async createEntry(
        createEdlEntryDto: CreateEdlEntryDto & { listId: string },
    ): Promise<EdlEntry> {
        // Check if the list exists
        const list = await this.prisma.edlList.findUnique({
            where: { id: createEdlEntryDto.listId },
        });
        if (!list) {
            throw new NotFoundException(
                `EDL List with ID ${createEdlEntryDto.listId} not found`,
            );
        }

        const entry = await this.prisma.edlEntry.create({
            data: {
                address: createEdlEntryDto.address,
                comment: createEdlEntryDto.comment,
                type: createEdlEntryDto.type,
                isEnabled: createEdlEntryDto.isEnabled ?? true,
                createdBy: createEdlEntryDto.createdBy,
                list: {
                    connect: { id: createEdlEntryDto.listId },
                },
            },
            include: { list: true },
        });
        return this.mapToEdlEntry(entry);
    }

    async updateEntry(
        entryId: string,
        updateEdlEntryDto: UpdateEdlEntryDto & { listId?: string },
    ): Promise<EdlEntry> {
        const existingEntry = await this.getEntry(entryId);

        // Verify the entry belongs to the specified list if listId is provided
        if (
            updateEdlEntryDto.listId &&
            existingEntry.listId !== updateEdlEntryDto.listId
        ) {
            throw new NotFoundException(
                `Entry ${entryId} does not belong to list ${updateEdlEntryDto.listId}`,
            );
        }

        const entry = await this.prisma.edlEntry.update({
            where: { id: entryId },
            data: {
                address: updateEdlEntryDto.address,
                comment: updateEdlEntryDto.comment,
                type: updateEdlEntryDto.type,
                isEnabled: updateEdlEntryDto.isEnabled,
                list: updateEdlEntryDto.listId
                    ? { connect: { id: updateEdlEntryDto.listId } }
                    : undefined,
            },
            include: { list: true },
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

    async getListEntries(id: string): Promise<EdlEntry[]> {
        const list = await this.prisma.edlList.findUnique({
            where: { id },
            include: { entries: true },
        });

        if (!list) {
            throw new NotFoundException(`EDL List ${id} not found`);
        }

        return list.entries.map((entry) => this.mapToEdlEntry(entry));
    }

    async deleteEntry(id: string): Promise<EdlEntry> {
        await this.getEntry(id);
        const entry = await this.prisma.edlEntry.delete({
            where: { id },
            include: { list: true },
        });
        return this.mapToEdlEntry(entry);
    }

    async getListPlaintext(id: string): Promise<string> {
        this.logger.debug(`Generating plaintext for EDL list: ${id}`);
        const list = await this.getList(id);

        return list.entries
            .filter((entry: EdlEntry) => entry.isEnabled)
            .map((entry: EdlEntry) => {
                switch (list.type) {
                    case ListType.IP:
                        return `${entry.address}`;
                    case ListType.DOMAIN:
                    case ListType.URL:
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
