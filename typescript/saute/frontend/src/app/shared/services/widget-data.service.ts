import { BehaviorSubject } from "rxjs";
import { Injectable } from "@angular/core";

@Injectable({
    providedIn: "root",
})
export class WidgetDataService {
    private dataSource = new BehaviorSubject<any[]>([]);

    currentData = this.dataSource.asObservable();

    constructor() {}

    changeData(data: any[]) {
        this.dataSource.next(data);
    }
}
